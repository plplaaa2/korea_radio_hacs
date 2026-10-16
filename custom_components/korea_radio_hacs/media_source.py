"""Korea Radio media browser.

Summary: Browse and resolve supported Korean radio channels.
Related files: api.py, const.py.
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

from .api import RadioEndpointManager
from .const import CHANNEL_MAPPING, DOMAIN


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
        """Resolve a radio channel to a playable stream URL."""
        if not (entries := self.hass.data.get(DOMAIN)):
            return None
        api: RadioEndpointManager = next(iter(entries.values()))
        channel = item.identifier.removeprefix("radio:")
        return PlayMedia(
            api.build_stream_link(channel, target_media_player=item.target_media_player),
            "audio/mpeg",
        )

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Browse supported radio channels."""
        if item.identifier in (None, "root", "radio_list"):
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier="radio_list",
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.MUSIC,
                title="Korea Radio",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=f"radio:{channel_id}",
                        media_class=MediaClass.MUSIC,
                        media_content_type="audio/mpeg",
                        title=name,
                        can_play=True,
                        can_expand=False,
                    )
                    for name, channel_id in CHANNEL_MAPPING.items()
                ],
            )
        return None
