"""Korea Radio API Client.

Summary: Validate the companion add-on connection and construct playback URLs.
Related files: config_flow.py, __init__.py, media_source.py, llm.py, const.py.
"""
from __future__ import annotations

import logging
from aiohttp import ClientError, ClientTimeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url
from .const import CHANNEL_MAPPING

_LOGGER = logging.getLogger(__name__)

class RadioEndpointManager:
    """Helper class for Korea Radio API interactions."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        token: str,
        radio_port: int,
        playback_host: str = "",
    ) -> None:
        """Initialize the API client."""
        self.hass = hass
        self.host = self._normalize_host(host)
        self.playback_host = self._normalize_host(playback_host) if playback_host else ""
        self.token = token
        self.radio_port = radio_port

    @staticmethod
    def _normalize_host(host: str) -> str:
        """Normalize a base URL and discard any separately configured port."""
        from urllib.parse import urlsplit

        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"
        parsed = urlsplit(host.rstrip("/"))
        if not parsed.hostname:
            raise ValueError("Host must contain a valid hostname or IP address")
        hostname = f"[{parsed.hostname}]" if ":" in parsed.hostname else parsed.hostname
        return f"{parsed.scheme}://{hostname}"

    async def async_validate_connection(self) -> None:
        """Validate the configured host, radio port, and authentication token."""
        from homeassistant.helpers.aiohttp_client import async_get_clientsession

        url = f"{self._resolve_host(self.radio_port)}/get_radio_list"
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                url,
                params={"token": self.token},
                timeout=ClientTimeout(total=10),
            ) as response:
                if response.status in (401, 403):
                    raise InvalidAuthError
                response.raise_for_status()
                await response.json()
        except ClientError:
            raise

    def _resolve_host(self, port: int, target_media_player: str | None = None) -> str:
        """Resolve host with specific port and HA internal IP check."""
        host = self.playback_host if target_media_player and self.playback_host else self.host
        if "localhost" in host or "127.0.0.1" in host:
            try:
                internal_url = get_url(self.hass, allow_internal=True, allow_ip=True, require_ssl=False)
                if internal_url:
                    ha_ip = internal_url.split("//")[1].split(":")[0]
                    host = f"http://{ha_ip}"
            except Exception as ex:
                _LOGGER.warning("Failed to resolve local IP: %s", ex)
        
        return f"{host}:{port}"

    def build_stream_link(
        self, channel_key: str, target_media_player: str | None = None
    ) -> str:
        """Generate a streaming URL for a given channel key (Radio)."""
        host_with_port = self._resolve_host(self.radio_port, target_media_player)
        channel = CHANNEL_MAPPING.get(channel_key, channel_key.lower())
        from urllib.parse import urlencode

        return f"{host_with_port}/radio?{urlencode({'keys': channel, 'token': self.token, 'atype': 1})}"

    def find_channel_title(self, channel_key: str) -> str:
        """Get a human-readable name for a channel key."""
        # Find the original key in mapping if it exists
        for k, v in CHANNEL_MAPPING.items():
            if v == channel_key.lower() or k.lower() == channel_key.lower():
                return k
        return channel_key

class InvalidAuthError(Exception):
    """Raised when the server rejects the configured token."""
