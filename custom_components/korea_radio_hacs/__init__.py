"""The Korea Radio integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import CONF_HOST, CONF_TOKEN, CONF_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .api import RadioEndpointManager

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Korea Radio component."""
    
    async def async_perform_radio_play(call: ServiceCall) -> None:
        """Handle the play_radio service call."""
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise ServiceValidationError("Korea Radio integration is not configured.")
        
        entry = next((e for e in entries if e.state == ConfigEntryState.LOADED), None)
        if not entry:
            raise ServiceValidationError("Korea Radio integration is not loaded.")

        # API Client initialization
        host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
        token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
        api = RadioEndpointManager(hass, host, token)

        entity_ids = call.data.get(CONF_ENTITY_ID)
        channel_raw = call.data.get("channel")
        
        if not entity_ids:
            raise ServiceValidationError("No entity_id provided.")

        if not isinstance(entity_ids, list):
            entity_ids = [entity_ids]

        stream_url = api.build_stream_link(channel_raw)
        title = f"Korea Radio: {api.find_channel_title(channel_raw)}"
        
        for entity_id in entity_ids:
            payload = {
                "entity_id": entity_id,
                "media_content_id": stream_url,
                "media_content_type": "audio/mpeg",
                "extra": {"metadata": {"metadataType": 3, "title": title}}
            }
            
            try:
                await hass.services.async_call("media_player", "play_media", payload)
            except Exception as ex:
                _LOGGER.error("Error calling play_media for %s: %s", entity_id, ex)

    hass.services.async_register(
        DOMAIN, "play_radio", async_perform_radio_play,
        schema=cv.make_entity_service_schema({vol.Required("channel"): cv.string})
    )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Korea Radio from a config entry."""
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    pass

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
