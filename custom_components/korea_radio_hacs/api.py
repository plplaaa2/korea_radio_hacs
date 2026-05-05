"""Korea Radio API Client."""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url
from .const import CHANNEL_MAPPING

_LOGGER = logging.getLogger(__name__)

class RadioEndpointManager:
    """Helper class for Korea Radio API interactions."""

    def __init__(self, hass: HomeAssistant, host: str, token: str, radio_port: int, tube_port: int) -> None:
        """Initialize the API client."""
        self.hass = hass
        # host에서 포트가 포함되어 있다면 제거 (IP/도메인만 유지)
        if ":" in host.replace("http://", ""):
            self.host = host.rsplit(":", 1)[0]
        else:
            self.host = host.rstrip("/")
        self.token = token
        self.radio_port = radio_port
        self.tube_port = tube_port

    def _resolve_host(self, port: int) -> str:
        """Resolve host with specific port and HA internal IP check."""
        host = self.host
        if "localhost" in host or "127.0.0.1" in host:
            try:
                internal_url = get_url(self.hass, allow_internal=True, allow_ip=True, require_ssl=False)
                if internal_url:
                    ha_ip = internal_url.split("//")[1].split(":")[0]
                    host = f"http://{ha_ip}"
            except Exception as ex:
                _LOGGER.warning("Failed to resolve local IP: %s", ex)
        
        return f"{host}:{port}"

    def build_stream_link(self, channel_key: str) -> str:
        """Generate a streaming URL for a given channel key (Radio)."""
        host_with_port = self._resolve_host(self.radio_port)
        channel = CHANNEL_MAPPING.get(channel_key, channel_key.lower())
        return f"{host_with_port}/radio?keys={channel}&token={self.token}&atype=1"

    def build_id_link(self, alias: str) -> str:
        """Generate a streaming URL using a TubePlayer Unique ID (Tube)."""
        host_with_port = self._resolve_host(self.tube_port)
        return f"{host_with_port}/tube?id={alias}&token={self.token}&atype=1"

    def find_channel_title(self, channel_key: str) -> str:
        """Get a human-readable name for a channel key."""
        # Find the original key in mapping if it exists
        for k, v in CHANNEL_MAPPING.items():
            if v == channel_key.lower() or k.lower() == channel_key.lower():
                return k
        return channel_key

    async def async_get_tube_list(self) -> list[dict[str, str]]:
        """Fetch the list of YouTube aliases from TubePlayer Lite server."""
        import aiohttp
        host_with_port = self._resolve_host(self.tube_port)
        url = f"{host_with_port}/api/list?token={self.token}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as ex:
            _LOGGER.error("Failed to fetch tube list: %s", ex)
        return []
