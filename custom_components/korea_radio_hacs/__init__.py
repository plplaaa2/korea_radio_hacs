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
    """Set up the Korea Radio component.
    - 연결된 파일: api.py (RadioEndpointManager API 제어 객체 호출)
    - 기능 요약: 공통 재생 서비스를 등록하고, hass.data에 캐싱된 API 클라이언트를 사용해 스트림 재생
    """
    
    async def async_perform_radio_play(call: ServiceCall) -> None:
        """Handle the play_radio and play_id service calls.
        - 연결된 파일: api.py (스트리밍 주소 빌드 메서드 사용)
        - 기능 요약: 미디어 플레이어에 스트리밍 주소 및 메타데이터를 전송하여 재생 명령
        """
        if DOMAIN not in hass.data or not hass.data[DOMAIN]:
            raise ServiceValidationError("Korea Radio integration is not configured or loaded.")
        
        # hass.data에 등록된 첫 번째 API 인스턴스 획득 (단일 인스턴스 전제)
        api = next(iter(hass.data[DOMAIN].values()))

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
    """Set up Korea Radio from a config entry.
    - 연결된 파일: api.py (RadioEndpointManager)
    - 기능 요약: 통합구성요소 셋업 시 API 관리 인스턴스를 초기화하여 hass.data에 등록
    """
    host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
    token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
    radio_port = entry.options.get(CONF_RADIO_PORT, entry.data.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT))
    tube_port = entry.options.get(CONF_TUBE_PORT, entry.data.get(CONF_TUBE_PORT, DEFAULT_TUBE_PORT))
    
    api = RadioEndpointManager(hass, host, token, radio_port, tube_port)
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.
    - 기능 요약: 통합구성요소 언로드 시 hass.data 내 저장된 캐시 인스턴스 정리
    """
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id)
    return True
