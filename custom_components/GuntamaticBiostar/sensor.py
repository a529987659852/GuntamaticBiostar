from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import BiostarUpdateCoordinator

# Import global values.
from .const import DOMAIN, MANUFACTURER, MODEL, SENSOR_DESC

# Import global values.
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensors for openWB."""

    integrationUniqueID = config.unique_id
    coordinator = hass.data[DOMAIN][config.entry_id]

    sensorList = []
    for sensor in SENSOR_DESC:
        sensorList.append(
            GuntamaticSensor(
                uniqueID=integrationUniqueID,
                device_friendly_name=integrationUniqueID,
                coordinator=coordinator,
                description=sensor,
            )
        )
    async_add_entities(sensorList)


class GuntamaticSensor(CoordinatorEntity[BiostarUpdateCoordinator], SensorEntity):
    entity_description: SensorEntityDescription

    def __init__(
        self,
        uniqueID: str | None,
        device_friendly_name: str,
        coordinator: BiostarUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = slugify(f"{uniqueID}-{description.name}")
        self.entity_id = f"sensor.{uniqueID}-{description.name}"
        self._sensor_data = coordinator.data
        self.device_friendly_name = device_friendly_name

    @property
    def native_value(self) -> StateType:
        try:
            return self._sensor_data.get(self.entity_description.key)[0]
        except:
            return self._sensor_data.get(self.entity_description.key)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information."""
        return DeviceInfo(
            name=self.device_friendly_name,
            identifiers={(DOMAIN, self.device_friendly_name)},
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._sensor_data = self.coordinator.data
        self.async_write_ha_state()
