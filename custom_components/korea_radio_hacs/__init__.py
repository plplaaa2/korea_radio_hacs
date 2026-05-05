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

from .const import DOMAIN, CONF_RADIO_PORT, CONF_TUBE_PORT, DEFAULT_RADIO_PORT, DEFAULT_TUBE_PORT
from .api import RadioEndpointManager

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Korea Radio component."""
    
    async def async_perform_radio_play(call: ServiceCall) -> None:
        """Handle the play_radio and play_id service calls."""
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise ServiceValidationError("Korea Radio integration is not configured.")
        
        entry = next((e for e in entries if e.state == ConfigEntryState.LOADED), None)
        if not entry:
            raise ServiceValidationError("Korea Radio integration is not loaded.")

        host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
        token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
        radio_port = entry.options.get(CONF_RADIO_PORT, entry.data.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT))
        tube_port = entry.options.get(CONF_TUBE_PORT, entry.data.get(CONF_TUBE_PORT, DEFAULT_TUBE_PORT))
        
        api = RadioEndpointManager(hass, host, token, radio_port, tube_port)

        entity_ids = call.data.get(CONF_ENTITY_ID)
        if not entity_ids:
            raise ServiceValidationError("No entity_id provided.")
        if not isinstance(entity_ids, list):
            entity_ids = [entity_ids]

        # 서비스 종류에 따른 URL 및 제목 결정 (엔드포인트 분리)
        if call.service == "play_id":
            alias = call.data.get("id")
            stream_url = api.build_id_link(alias)
            title = f"YouTube: {alias}"
        else:
            channel_raw = call.data.get("channel")
            stream_url = api.build_stream_link(channel_raw)
            title = f"Radio: {api.find_channel_title(channel_raw)}"
        
        for entity_id in entity_ids:
            payload = {
                "entity_id": entity_id,
                "media_content_id": stream_url,
                "media_content_type": "music",
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
    hass.services.async_register(
        DOMAIN, "play_id", async_perform_radio_play,
        schema=cv.make_entity_service_schema({vol.Required("id"): cv.string})
    )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Korea Radio from a config entry."""
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
