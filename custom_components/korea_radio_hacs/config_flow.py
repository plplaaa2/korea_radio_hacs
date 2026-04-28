import voluptuous as vol
import logging
from homeassistant import config_entries
from .const import DOMAIN, TITLE, CONF_HOST, CONF_TOKEN, DEFAULT_TOKEN

_LOGGER = logging.getLogger(__name__)

class KoreaRadioOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Korea Radio options."""
    def __init__(self, entry):
        """Initialize options flow."""
        super().__init__()
        self._entry = entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_host = self._entry.options.get(
            CONF_HOST, self._entry.data.get(CONF_HOST, "http://localhost:3005")
        )
        current_token = self._entry.options.get(
            CONF_TOKEN, self._entry.data.get(CONF_TOKEN, DEFAULT_TOKEN)
        )

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=current_host): str,
            vol.Required(CONF_TOKEN, default=current_token): str,
        })
        return self.async_show_form(step_id="init", data_schema=schema)


class KoreaRadioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Korea Radio."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=TITLE, data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST, default="http://localhost:3005"): str,
            vol.Required(CONF_TOKEN, default=DEFAULT_TOKEN): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KoreaRadioOptionsFlowHandler(config_entry)
