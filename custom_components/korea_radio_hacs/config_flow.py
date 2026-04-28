import voluptuous as vol
import logging
from homeassistant import config_entries
from .const import DOMAIN, TITLE, CONF_HOST, CONF_TOKEN, DEFAULT_TOKEN

_LOGGER = logging.getLogger(__name__)

# Options Flow: 재구성 시 설정 변경
class KRadioOptionsProvider(config_entries.OptionsFlow):
    def __init__(self, entry):
        super().__init__()
        self._entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # 현재 설정값 가져오기 (options에 없으면 data에서)
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


# Config Flow: 최초 등록
class KRadioSetupFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
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
        return KRadioOptionsProvider(config_entry)
