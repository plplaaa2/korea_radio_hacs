import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_HOST, CONF_TOKEN, CONF_RADIO_PORT, CONF_TUBE_PORT, DEFAULT_RADIO_PORT, DEFAULT_TUBE_PORT

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
        current_tube_port = self._entry.options.get(
            CONF_TUBE_PORT, self._entry.data.get(CONF_TUBE_PORT, DEFAULT_TUBE_PORT)
        )

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=current_host): str,
            vol.Required(CONF_TOKEN, default=current_token): str,
            vol.Required(CONF_RADIO_PORT, default=current_radio_port): int,
            vol.Required(CONF_TUBE_PORT, default=current_tube_port): int,
        })
        return self.async_show_form(step_id="init", data_schema=schema)


class KoreaRadioHacsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Korea Radio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Korea Radio Hacs", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST, default="http://localhost"): str,
            vol.Required(CONF_TOKEN, default="homeassistant"): str,
            vol.Required(CONF_RADIO_PORT, default=DEFAULT_RADIO_PORT): int,
            vol.Required(CONF_TUBE_PORT, default=DEFAULT_TUBE_PORT): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KoreaRadioOptionsFlowHandler(config_entry)
