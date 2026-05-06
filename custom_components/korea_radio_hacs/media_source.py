"""Korea Radio Media Source.
- 연결된 파일: api.py, const.py
"""
from __future__ import annotations

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState

from .const import DOMAIN, CHANNEL_MAPPING, CONF_HOST, CONF_TOKEN, CONF_RADIO_PORT, CONF_TUBE_PORT, DEFAULT_RADIO_PORT, DEFAULT_TUBE_PORT
from .api import RadioEndpointManager

async def async_get_media_source(hass: HomeAssistant) -> MediaSource:
    """Set up Korea Radio media source."""
    return RadioChannelBrowser(hass)

class RadioChannelBrowser(MediaSource):
    """Provide Korea Radio channels as media sources."""

    name: str = "Korea Radio"

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize Korea Radio media source."""
        super().__init__(DOMAIN)
        self.hass = hass

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a media item to a playable URL."""
        entries = self.hass.config_entries.async_entries(DOMAIN)
        entry = next((e for e in entries if e.state == ConfigEntryState.LOADED), None)
        if not entry: return None

        host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
        token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
        radio_port = entry.options.get(CONF_RADIO_PORT, entry.data.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT))
        tube_port = entry.options.get(CONF_TUBE_PORT, entry.data.get(CONF_TUBE_PORT, DEFAULT_TUBE_PORT))
        
        api = RadioEndpointManager(self.hass, host, token, radio_port, tube_port)
        
        identifier = item.identifier
        if identifier.startswith("tube:"):
            url = api.build_id_link(identifier.replace("tube:", ""))
        else:
            # 기본은 라디오로 처리 (radio: 접두사 대응 및 레거시 대응)
            clean_id = identifier.replace("radio:", "")
            url = api.build_stream_link(clean_id)
        
        return PlayMedia(url, "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Browse media."""
        if item.identifier in (None, "root"):
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier="root",
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.MUSIC,
                title="Korea Radio & Tube",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier="radio_list",
                        media_class=MediaClass.DIRECTORY,
                        media_content_type=MediaType.MUSIC,
                        title="Radio Channels",
                        can_play=False,
                        can_expand=True,
                    ),
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier="tube_list",
                        media_class=MediaClass.DIRECTORY,
                        media_content_type=MediaType.MUSIC,
                        title="TubePlayer Music",
                        can_play=False,
                        can_expand=True,
                    ),
                ],
            )
        
        if item.identifier == "radio_list":
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier="radio_list",
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.MUSIC,
                title="Radio Channels",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=f"radio:{channel_id}",
                        media_class=MediaClass.MUSIC,
                        media_content_type=MediaType.MUSIC,
                        title=name,
                        can_play=True,
                        can_expand=False,
                    )
                    for name, channel_id in CHANNEL_MAPPING.items()
                ],
            )

        if item.identifier == "tube_list":
            # TubePlayer 목록 실시간 조회
            entries = self.hass.config_entries.async_entries(DOMAIN)
            entry = next((e for e in entries if e.state == ConfigEntryState.LOADED), None)
            if not entry: return None

            host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
            token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
            radio_port = entry.options.get(CONF_RADIO_PORT, entry.data.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT))
            tube_port = entry.options.get(CONF_TUBE_PORT, entry.data.get(CONF_TUBE_PORT, DEFAULT_TUBE_PORT))
            api = RadioEndpointManager(self.hass, host, token, radio_port, tube_port)
            
            tube_items = await api.async_get_tube_list()
            
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier="tube_list",
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.MUSIC,
                title="TubePlayer Music",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=f"tube:{t['id']}",
                        media_class=MediaClass.MUSIC,
                        media_content_type=MediaType.MUSIC,
                        title=t['name'],
                        can_play=True,
                        can_expand=False,
                    )
                    for t in tube_items
                ],
            )
            
        return None
