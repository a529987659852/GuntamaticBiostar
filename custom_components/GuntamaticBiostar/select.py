from __future__ import annotations

import logging

from homeassistant.components.select import DOMAIN as ENTITY_DOMAIN, SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from . import BiostarUpdateCoordinator

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    SELECT_DESC,
    guntamaticSelectEntityDescription,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    integrationUniqueID = config.unique_id
    coordinator = hass.data[DOMAIN][config.entry_id]

    sensorList = []
    for sensor in SELECT_DESC:
        sensorList.append(
            GuntamaticSelect(
                uniqueID=integrationUniqueID,
                device_friendly_name=integrationUniqueID,
                coordinator=coordinator,
                description=sensor,
            )
        )
    async_add_entities(sensorList)


class GuntamaticSelect(CoordinatorEntity[BiostarUpdateCoordinator], SelectEntity):

    entity_description: guntamaticSelectEntityDescription

    def __init__(
        self,
        uniqueID: str | None,
        device_friendly_name: str,
        coordinator: BiostarUpdateCoordinator,
        description: guntamaticSelectEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = slugify(f"{uniqueID}-{description.name}")
        self.entity_id = f"{ENTITY_DOMAIN}.{uniqueID}-{description.name}"
        self._sensor_data = coordinator.data
        self.device_friendly_name = device_friendly_name

        self._attr_options = description.modes
        self._attr_current_option = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information."""
        return DeviceInfo(
            name=self.device_friendly_name,
            identifiers={(DOMAIN, self.device_friendly_name)},
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    async def async_select_option(self, option: str) -> None:
        result = await self.coordinator.setProgram(
            self.entity_description.optionsMapping.get(option)
        )
        if result:
            self._attr_current_option = option
            self.async_write_ha_state()
            _LOGGER.debug(f"Biostar heating program set to {option}.")
        else:
            _LOGGER.error(f"Error changing Biostar heating program to {option}.")
