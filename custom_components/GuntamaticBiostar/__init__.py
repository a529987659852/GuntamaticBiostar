"""The GuntamaticBiostar component for controlling the Guntamatic Biostar heating via home assistant / API"""
import logging
from datetime import timedelta
from typing import Any

import async_timeout
from aiohttp import ClientSession
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

# Import global values.
from .const import DATA_SCHEMA_API_KEY, DATA_SCHEMA_HOST, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    websession = async_get_clientsession(hass)
    api_key = entry.data[DATA_SCHEMA_API_KEY]
    host = entry.data[DATA_SCHEMA_HOST]
    coordinator = BiostarUpdateCoordinator(
        hass=hass, session=websession, api_key=api_key, host=host
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Trigger the creation of sensors.
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    # Return boolean to indicate that initialization was successfully.
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload all sensor entities and services if integration is removed via UI.
    No restart of home assistant is required."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok


class ApiError(Exception):
    """Raised when AccuWeather API request ended in error."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status


class Biostar:
    def __init__(
        self,
        api_key: str,
        host: str,
        session: ClientSession,
    ):
        self._api_key = api_key
        self._host = host
        self._session = session

    async def _async_get_data(self) -> dict[str, Any]:
        """Retrieve data from AccuWeather API."""
        params = {"key": self._api_key}
        async with self._session.get(
            f"http://{self._host}/ext/daqdesc.cgi", params=params
        ) as resp:
            if resp.status != 200:
                # error_text = json.loads(await resp.text())
                raise ApiError(f"Invalid response from Biostar API: {resp.status}")
            _LOGGER.debug("Data retrieved from Biostar, status: %s", resp.status)

            dataDescription = await resp.json()
            # dataDescription = dataDescription.split('\n')[0:-1]

        async with self._session.get(
            f"http://{self._host}/ext/daqdata.cgi", params=params
        ) as resp:
            if resp.status != 200:
                # error_text = json.loads(await resp.text())
                raise ApiError(f"Invalid response from Biostar API: {resp.status}")
            _LOGGER.debug("Data retrieved from Bioestar, status: %s", resp.status)
            dataValues = await resp.json()
            # dataValues = dataValues.split('\n')[0:-1]

        data = {}
        for i in range(len(dataDescription)):
            key = dataDescription[i].get("name")
            unitOfMeasurement = dataDescription[i].get("unit")
            dataValue = dataValues[i]
            data[key] = [dataValue, unitOfMeasurement]

        return data


class BiostarUpdateCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        api_key: str,
        host: str,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=1),
        )
        self.my_api = Biostar(api_key=api_key, session=session, host=host)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(5):
                currentData = await self.my_api._async_get_data()
        except:
            raise UpdateFailed

        return currentData
