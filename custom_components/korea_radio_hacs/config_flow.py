"""Config flow for Korea Radio integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class KoreaRadioOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Korea Radio options."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # 현재 설정값 가져오기
        current_host = self.config_entry.options.get(
            "host", self.config_entry.data.get("host", "http://localhost:3005")
        )
        current_token = self.config_entry.options.get(
            "token", self.config_entry.data.get("token", "homeassistant")
        )

        schema = vol.Schema({
            vol.Required("host", default=current_host): str,
            vol.Required("token", default=current_token): str,
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
            vol.Required("host", default="http://localhost:3005"): str,
            vol.Required("token", default="homeassistant"): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        
        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                data={**entry.data, **user_input},
                reason="reconfigure_successful",
            )

        schema = vol.Schema({
            vol.Required("host", default=entry.data.get("host")): str,
            vol.Required("token", default=entry.data.get("token")): str,
        })
        return self.async_show_form(step_id="reconfigure", data_schema=schema)

    @callback
    def async_get_options_flow(self, config_entry: config_entries.ConfigEntry) -> KoreaRadioOptionsFlowHandler:
        """Get the options flow for this handler."""
        return KoreaRadioOptionsFlowHandler(config_entry)
