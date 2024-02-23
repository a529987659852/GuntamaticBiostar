"""The GuntamaticBiostar component for controlling the Guntamatic Biostar heating via home assistant / API"""
from __future__ import annotations

from dataclasses import dataclass
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    # BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.components.select import SelectEntityDescription

from homeassistant.const import (
    PERCENTAGE,
    Platform,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
)
from homeassistant.helpers.entity import EntityCategory

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SELECT,
]

# Global values
DOMAIN = "GuntamaticBiostar"
MANUFACTURER = "Guntamatic"
MODEL = "Biostar"
DATA_SCHEMA_HOST = "host"
DATA_SCHEMA_API_KEY = "api_key"

# Data schema required by configuration flow
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(DATA_SCHEMA_HOST): cv.string,
        vol.Required(DATA_SCHEMA_API_KEY): cv.string,
    }
)


@dataclass
class guntamaticSelectEntityDescription(SelectEntityDescription):
    """Enhance the select entity description for Guntamatic"""

    optionsMapping: dict | None = None
    modes: list | None = None


SENSOR_DESC = [
    SensorEntityDescription(
        key="Aussentemperatur",
        name="Außentemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:sun-thermometer-outline",
    ),
    SensorEntityDescription(
        key="Kesseltemperatur",
        name="Kesseltemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Leistung",
        name="Leistung",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="CO2 Gehalt",
        name="CO2-Gehalt",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Puffer oben",
        name="Puffer oben",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-chevron-up",
    ),
    SensorEntityDescription(
        key="Puffer unten",
        name="Puffer unten",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-chevron-down",
    ),
    SensorEntityDescription(
        key="Warmwasser 0",
        name="Warmwasser 0",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Raumtemp. HK 1",
        name="Raumtemp. HK 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Ist 1",
        name="Vorlauf Ist 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Ist 2",
        name="Vorlauf Ist 2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Betriebszeit",
        name="Betriebszeit",
        # device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="Servicezeit",
        name="Servicezeit",
        # device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:account-wrench",
    ),
    SensorEntityDescription(
        key="Asche leeren in",
        name="Asche leeren in",
        # device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:delete-empty",
    ),
    SensorEntityDescription(
        key="Vorlauf Ist 0",
        name="Vorlauf Ist 0",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Brennstoffzähler",
        name="Brennstoffzähler",
        device_class=None,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="Pufferladung",
        name="Pufferladung",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Betriebscode",
        name="Betriebscode",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Programm",
        name="Programm",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        # entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
    ),
    SensorEntityDescription(
        key="Progamm HK0",
        name="Programm HK0",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        # entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
    ),
    SensorEntityDescription(
        key="Progamm HK1",
        name="Programm HK1",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        # entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
    ),
    SensorEntityDescription(
        key="Progamm HK2",
        name="Programm HK2",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        # entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
    ),
    # Daten vom alten API
    SensorEntityDescription(
        key="Austragmotor",
        name="Austragmotor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="CO2 Soll",
        name="CO2 Soll",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=PERCENTAGE,
        state_class=None,
    ),
    SensorEntityDescription(
        key="Kesselsolltemp",
        name="Kesselsolltemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=None,
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="Rauchgasauslastung",
        name="Rauchgasauslastung",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="Rost",
        name="Rost",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="Rücklauftemp. Soll",
        name="Rücklauftemperatur Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=None,
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="Rücklauftemp.",
        name="Rücklauftemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Saugzuggebläse",
        name="Saugzuggebläse",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="Vorlauf Soll 1",
        name="Vorlauf Soll 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=None,
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="Vorlauf Soll 2",
        name="Vorlauf Soll 2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=None,
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="Wirkungsgrad",
        name="Wirkungsgrad",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="Störung 0",
        name="Störung 0",
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:alert-circle",
    ),
    SensorEntityDescription(
        key="Störung 1",
        name="Störung 1",
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:alert-circle",
    ),
    SensorEntityDescription(
        key="Kesselzustand-Nr.",
        name="Kesselzustand-Nr.",
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Version",
        name="Version",
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_visible_default=False,
    ),
    SensorEntityDescription(
        key="Serial",
        name="Serial",
        state_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_visible_default=False,
    ),
    SensorEntityDescription(
        key="Betrieb",
        name="Betrieb",
        state_class=None,
        entity_registry_visible_default=True,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
    ),
]

BINARY_SENSOR_DESC = [
    BinarySensorEntityDescription(
        key="Pumpe HP0",
        name="Pumpe HP0",
    ),
    BinarySensorEntityDescription(
        key="P Warmwasser 0",
        name="P Warmwasser 0",
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 0",
        name="Heizkreis 0",
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 1",
        name="Heizkreis 1",
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 2",
        name="Heizkreis 2",
    ),
    BinarySensorEntityDescription(
        key="Kesselfreigabe",
        name="Kesselfreigabe",
    ),
    # Daten vom alten API
    BinarySensorEntityDescription(
        key="Austragungsgebläse",
        name="Austragungsgebläse",
    ),
    BinarySensorEntityDescription(
        key="Füllstand",
        name="Füllstand",
    ),
    BinarySensorEntityDescription(
        key="Mischer 1",
        name="Mischer 1",
    ),
    BinarySensorEntityDescription(
        key="Mischer 2",
        name="Mischer 2",
    ),
]

SELECT_DESC = [
    guntamaticSelectEntityDescription(
        key="Program",
        name="Program",
        icon="mdi:cog",
        modes=[
            "AUS",
            "NORMAL",
            "WARMWASSER",
            "WW NACHLADEN",
        ],
        optionsMapping={"AUS": 0, "NORMAL": 1, "WARMWASSER": 2, "WW NACHLADEN": 6},
    ),
]
