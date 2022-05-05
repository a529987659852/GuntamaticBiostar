"""The GuntamaticBiostar component for controlling the Guntamatic Biostar heating via home assistant / API"""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import BiostarUpdateCoordinator

# Import global values.
from .const import BINARY_SENSOR_DESC, DOMAIN, MANUFACTURER, MODEL


async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensors for openWB."""

    integrationUniqueID = config.unique_id
    coordinator = hass.data[DOMAIN][config.entry_id]

    sensorList = []
    for sensor in BINARY_SENSOR_DESC:
        sensorList.append(
            GuntamaticBinarySensor(
                uniqueID=integrationUniqueID,
                device_friendly_name=integrationUniqueID,
                coordinator=coordinator,
                description=sensor,
            )
        )
    async_add_entities(sensorList)


class GuntamaticBinarySensor(
    CoordinatorEntity[BiostarUpdateCoordinator], BinarySensorEntity
):
    entity_description: BinarySensorEntityDescription

    def __init__(
        self,
        uniqueID: str | None,
        device_friendly_name: str,
        coordinator: BiostarUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = slugify(f"{uniqueID}-{description.name}")
        self.entity_id = f"binary_sensor.{uniqueID}-{description.name}"
        self._sensor_data = coordinator.data
        self.device_friendly_name = device_friendly_name

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information."""
        return DeviceInfo(
            name=self.device_friendly_name,
            identifiers={(DOMAIN, self.device_friendly_name)},
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    @property
    def is_on(self) -> bool | None:
        return self._sensor_data.get(self.entity_description.key)[0]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._sensor_data = self.coordinator.data
        self.async_write_ha_state()
