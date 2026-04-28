"""Korea Radio Media Source."""
from __future__ import annotations

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant, ConfigEntryState

from .const import DOMAIN, CHANNEL_MAPPING, CONF_HOST, CONF_TOKEN
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
        
        if not entry:
            return None

        host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, ""))
        token = entry.options.get(CONF_TOKEN, entry.data.get(CONF_TOKEN, ""))
        
        api = RadioEndpointManager(self.hass, host, token)
        url = api.build_stream_link(item.identifier)
        
        return PlayMedia(url, "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Browse media."""
        if item.identifier is None:
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier="root",
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.CHANNELS,
                title="Korea Radio",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=channel_id,
                        media_class=MediaClass.MUSIC,
                        media_content_type=MediaType.MUSIC,
                        title=name,
                        can_play=True,
                        can_expand=False,
                    )
                    for name, channel_id in CHANNEL_MAPPING.items()
                ],
            )
        return None
