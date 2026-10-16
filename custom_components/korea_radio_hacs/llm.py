"""Selectable Korea Radio LLM API; related files: api.py, const.py, __init__.py."""
from __future__ import annotations

import probatio

from homeassistant.components.homeassistant import async_should_expose
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.llm import (
    API,
    APIInstance,
    LLMContext,
    Tool,
    ToolAnnotations,
    ToolInput,
    ToolResult,
)

from .const import CHANNEL_MAPPING, DOMAIN


class PlayRadioTool(Tool):
    """Play a Korean radio station on an exposed media player."""

    name = "korea_radio"
    title = "Korea Radio"
    description = (
        "Play a Korean radio station on an Assist-exposed Home Assistant media player. "
        "Use a channel key such as kbs_cool, kbs_happy, kbs_classic, mbc_fm4u, "
        "mbc_fm, sbs_power, sbs_love, cbs_music, cbs_fm, ytn, tbs, tbn, ifm, "
        "kfn, obs, wbs, or ebs, and the target media player entity ID."
    )
    integration = DOMAIN
    annotations = ToolAnnotations(
        read_only=False,
        destructive=False,
        idempotent=False,
        open_world=True,
    )
    parameters = probatio.Schema(
        {
            probatio.Required("channel"): str,
            probatio.Required("entity_id"): str,
        }
    )

    def __init__(self, entry_id: str) -> None:
        self._entry_id = entry_id

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: ToolInput,
        llm_context: LLMContext,
    ) -> ToolResult:
        """Start the requested station on the exposed media player."""
        channel = tool_input.tool_args["channel"].strip().lower()
        entity_id = tool_input.tool_args["entity_id"]
        if not entity_id.startswith("media_player."):
            raise HomeAssistantError("The target must be a media player entity")
        if channel not in {value.lower() for value in CHANNEL_MAPPING.values()}:
            raise HomeAssistantError(f"Unsupported Korea Radio channel: {channel}")
        if not async_should_expose(hass, llm_context.assistant, entity_id):
            raise HomeAssistantError("The target media player is not exposed to Assist")
        if not (api := hass.data.get(DOMAIN, {}).get(self._entry_id)):
            raise HomeAssistantError("Korea Radio is not configured")
        await hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": entity_id,
                "media_content_id": api.build_stream_link(
                    channel, target_media_player=entity_id
                ),
                "media_content_type": "music",
                "extra": {
                    "metadata": {
                        "metadataType": 3,
                        "title": f"Radio: {api.find_channel_title(channel)}",
                    }
                },
            },
            context=llm_context.context,
            blocking=True,
        )
        return ToolResult(data={"message": f"Started {channel} on {entity_id}"})


class KoreaRadioAPI(API):
    """Expose radio playback as a separately selectable conversation provider."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        super().__init__(hass=hass, id=f"{DOMAIN}_{entry_id}", name="Korea Radio")
        self._entry_id = entry_id

    async def async_get_api_instance(self, llm_context: LLMContext) -> APIInstance:
        if self._entry_id not in self.hass.data.get(DOMAIN, {}):
            raise HomeAssistantError("Korea Radio is not configured")
        return APIInstance(
            api=self,
            api_prompt=(
                "Use korea_radio when asked to play a Korean radio station. "
                "Supported keys: kbs_cool, kbs_happy, kbs_classic, kbs_1radio, "
                "kbs_3radio, mbc_fm4u, mbc_fm, sbs_power, sbs_love, cbs_music, "
                "cbs_fm, ytn, tbs, tbn, ifm, kfn, obs, wbs, ebs. "
                "Only target media players exposed to Assist."
            ),
            llm_context=llm_context,
            tools=[PlayRadioTool(self._entry_id)],
        )


@callback
def async_get_tools(hass: HomeAssistant, llm_context: LLMContext, api_id: str) -> None:
    """Avoid injecting duplicate tools into the built-in Assist API."""
    return None


@callback
def register_api(hass: HomeAssistant, entry_id: str):
    """Register one selectable provider for this config entry."""
    from homeassistant.helpers.llm import async_register_api

    return async_register_api(hass, KoreaRadioAPI(hass, entry_id))
