"""Korea Radio setup and options flows.

Summary: Validate server settings and prevent duplicate server entries.
Related files: api.py, const.py, strings.json, translations/ko.json.
"""

import logging
from urllib.parse import urlsplit
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_HOST, CONF_TOKEN, CONF_RADIO_PORT, CONF_PLAYBACK_HOST, DEFAULT_RADIO_PORT
from .api import InvalidAuthError, RadioEndpointManager

_LOGGER = logging.getLogger(__name__)

class KoreaRadioOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Korea Radio options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        super().__init__()
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # 현재 설정값 가져오기 (options 우선, 없으면 data에서 가져옴)
        current_host = self._entry.options.get(
            CONF_HOST, self._entry.data.get(CONF_HOST, "http://localhost")
        )
        current_token = self._entry.options.get(
            CONF_TOKEN, self._entry.data.get(CONF_TOKEN, "homeassistant")
        )

        current_radio_port = self._entry.options.get(
            CONF_RADIO_PORT, self._entry.data.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT)
        )
        current_playback_host = self._entry.options.get(
            CONF_PLAYBACK_HOST, self._entry.data.get(CONF_PLAYBACK_HOST, "")
        )
        schema = vol.Schema({
            vol.Required(CONF_HOST, default=current_host): str,
            vol.Required(CONF_TOKEN, default=current_token): str,
            vol.Required(CONF_RADIO_PORT, default=current_radio_port): int,
            vol.Optional(CONF_PLAYBACK_HOST, default=current_playback_host): str,
        })
        return self.async_show_form(step_id="init", data_schema=schema)


class KoreaRadioHacsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Korea Radio."""

    VERSION = 3

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            errors = {}
            try:
                api = RadioEndpointManager(
                    self.hass,
                    user_input[CONF_HOST],
                    user_input[CONF_TOKEN],
                    user_input[CONF_RADIO_PORT],
                    user_input.get(CONF_PLAYBACK_HOST, ""),
                )
                await api.async_validate_connection()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception as err:
                _LOGGER.warning("Unable to validate Korea Radio server: %s", err)
                errors["base"] = "cannot_connect"
            else:
                host = user_input[CONF_HOST].strip().rstrip("/")
                parsed = urlsplit(host if "://" in host else f"http://{host}")
                await self.async_set_unique_id(
                    f"{parsed.hostname or host}:{user_input[CONF_RADIO_PORT]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Korea Radio", data=user_input)
            return self.async_show_form(
                step_id="user",
                data_schema=self._user_schema(user_input),
                errors=errors,
            )

        return self.async_show_form(step_id="user", data_schema=self._user_schema())

    @staticmethod
    def _user_schema(user_input=None):
        """Build the initial configuration schema, preserving submitted values."""
        values = user_input or {}
        return vol.Schema({
            vol.Required(CONF_HOST, default=values.get(CONF_HOST, "http://localhost")): str,
            vol.Required(CONF_TOKEN, default=values.get(CONF_TOKEN, "homeassistant")): str,
            vol.Required(CONF_RADIO_PORT, default=values.get(CONF_RADIO_PORT, DEFAULT_RADIO_PORT)): int,
            vol.Optional(CONF_PLAYBACK_HOST, default=values.get(CONF_PLAYBACK_HOST, "")): str,
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KoreaRadioOptionsFlowHandler(config_entry)
