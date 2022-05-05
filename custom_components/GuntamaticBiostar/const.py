"""The GuntamaticBiostar component for controlling the Guntamatic Biostar heating via home assistant / API"""
from __future__ import annotations

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS,
    TIME_DAYS,
    TIME_HOURS,
    VOLUME_CUBIC_METERS,
    Platform,
)
from homeassistant.helpers.entity import EntityCategory

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
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

SENSOR_DESC = [
    SensorEntityDescription(
        key="Aussentemperatur",
        name="Außentemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Kesseltemperatur",
        name="Kesseltemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Leistung",
        name="Leistung",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Puffer unten",
        name="Puffer unten",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Warmwasser 0",
        name="Warmwasser 0",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # SensorEntityDescription(
    #     key="Raumtemp. HK 0",
    #     name="Raumtemp. HK 0",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     native_unit_of_measurement=TEMP_CELSIUS,
    #     state_class=SensorStateClass.MEASUREMENT,
    # ),
    SensorEntityDescription(
        key="Vorlauf Ist 1",
        name="Vorlauf Ist 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Ist 2",
        name="Vorlauf Ist 2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Betriebszeit",
        name="Betriebszeit",
        #   device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=TIME_HOURS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Servicezeit",
        name="Servicezeit",
        # device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=TIME_DAYS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Asche leeren in",
        name="Asche leeren in",
        # device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=TIME_HOURS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Ist 0",
        name="Vorlauf Ist 0",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Brennstoffzähler",
        name="Brennstoffzähler",
        device_class=None,
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.MEASUREMENT,
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
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Programm",
        name="Programm",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Progamm HK0",
        name="Programm HK0",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Progamm HK1",
        name="Programm HK1",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Progamm HK2",
        name="Programm HK2",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Daten vom alten API
    SensorEntityDescription(
        key="Austragmotor",
        name="Austragmotor",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="CO2 Soll",
        name="CO2 Soll",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Kesselsolltemp",
        name="Kesselsolltemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Rauchgasauslastung",
        name="Rauchgasauslastung",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Rost",
        name="Rost",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Rücklauftemp. Soll",
        name="Rücklauftemperatur Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Rücklauftemp.",
        name="Rücklauftemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Saugzuggebläse",
        name="Saugzuggebläse",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Soll 1",
        name="Vorlauf Soll 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Vorlauf Soll 2",
        name="Vorlauf Soll 2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Wirkungsgrad",
        name="Wirkungsgrad",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Störung 0",
        name="Störung 0",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Störung 1",
        name="Störung 1",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Kesselzustand-Nr.",
        name="Kesselzustand-Nr.",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="Version",
        name="Version",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_visible_default=False,
    ),
    SensorEntityDescription(
        key="Serial",
        name="Serial",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_visible_default=False,
    ),
]

BINARY_SENSOR_DESC = [
    BinarySensorEntityDescription(
        key="Pumpe HP0",
        name="Pumpe HP0",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="P Warmwasser 0",
        name="P Warmwasser 0",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 0",
        name="Heizkreis 0",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 1",
        name="Heizkreis 1",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Heizkreis 2",
        name="Heizkreis 2",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Kesselfreigabe",
        name="Kesselfreigabe",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    # Daten vom alten aPI
    BinarySensorEntityDescription(
        key="Austragungsgebläse",
        name="Austragungsgebläse",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Füllstand",
        name="Füllstand",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Mischer 1",
        name="Mischer 1",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="Mischer 2",
        name="Mischer 2",
        device_class=BinarySensorDeviceClass.POWER,
    ),
]
