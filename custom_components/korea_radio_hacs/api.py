"""Korea Radio API Client."""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url
from .const import CHANNEL_MAPPING

_LOGGER = logging.getLogger(__name__)

class RadioEndpointManager:
    """Helper class for Korea Radio API interactions."""

    def __init__(self, hass: HomeAssistant, host: str, token: str) -> None:
        """Initialize the API client."""
        self.hass = hass
        self.host = host.rstrip("/")
        self.token = token

    def build_stream_link(self, channel_key: str) -> str:
        """Generate a streaming URL for a given channel key."""
        # Convert host if it's localhost to HA internal IP for external device compatibility
        host = self.host
        if "localhost" in host or "127.0.0.1" in host:
            try:
                internal_url = get_url(self.hass, allow_internal=True, allow_ip=True, require_ssl=False)
                if internal_url:
                    ha_ip = internal_url.split("//")[1].split(":")[0]
                    if ":" in host.replace("http://", ""):
                        port = host.split(":")[-1]
                        host = f"http://{ha_ip}:{port}"
                    else:
                        host = f"http://{ha_ip}"
                    _LOGGER.debug("Converted localhost to %s for external device compatibility", host)
            except Exception as ex:
                _LOGGER.warning("Failed to resolve local IP for Google Cast: %s", ex)

        # Map channel key if necessary
        channel = CHANNEL_MAPPING.get(channel_key, channel_key.lower())
        
        return f"{host}/radio?keys={channel}&token={self.token}&atype=1"

    def find_channel_title(self, channel_key: str) -> str:
        """Get a human-readable name for a channel key."""
        # Find the original key in mapping if it exists
        for k, v in CHANNEL_MAPPING.items():
            if v == channel_key.lower() or k.lower() == channel_key.lower():
                return k
        return channel_key
