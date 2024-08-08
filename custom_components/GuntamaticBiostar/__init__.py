"""The GuntamaticBiostar component for controlling the Guntamatic Biostar heating via home assistant / API"""
import logging
from datetime import timedelta
from typing import Any
import json

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
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Return boolean to indicate that initialization was successfully.
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload all sensor entities and services if integration is removed via UI.
    No restart of home assistant is required."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok


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
        """Retrieve data from Guntamatic API."""
        data = {}
        params = {"key": self._api_key}
        # Get data from new API
        APIEndpoints = ["/ext/daqdesc.cgi", "/ext/daqdata.cgi"]
        for API in APIEndpoints:
            async with self._session.get(
                f"http://{self._host}{API}", params=params
            ) as resp:
                if not resp.status == 200:
                    _LOGGER.error(
                        f"Invalid response from Biostar API: {API}, {resp.status}"
                    )
                    raise UpdateFailed

                r = await resp.text()

                if API == APIEndpoints[0]:
                    dataDescription = json.loads(r.replace(',,', ','))
                elif API == APIEndpoints[1]:
                    dataValues = json.loads(r.replace(',,', ','))

        for i in range(len(dataDescription)):
            key = dataDescription[i].get("name")
            unitOfMeasurement = dataDescription[i].get("unit")
            dataValue = dataValues[i]
            data[key] = [dataValue, unitOfMeasurement]

        # Get data from old API
        APIEndpoints = [
            "/daqdesc.cgi",
            "/daqdata.cgi",
        ]
        for API in APIEndpoints:
            async with self._session.get(
                f"http://{self._host}{API}", params=params
            ) as resp:
                if not resp.status == 200:
                    _LOGGER.error(f"Invalid response from Biostar API: {resp.status}")
                    raise UpdateFailed

                if API == APIEndpoints[0]:
                    dataDescription = await resp.text(encoding="windows-1252")
                    dataDescription = dataDescription.split("\n")[0:-1]
                elif API == APIEndpoints[1]:
                    dataValues = await resp.text(encoding="windows-1252")
                    dataValues = dataValues.split("\n")[0:-1]

        for i in range(len(dataDescription)):
            key, unitOfMeasurement = dataDescription[i].split(";")
            if (
                key == "reserved" or key in data
            ):  # value is not displayed or already exists in new API
                continue
            if unitOfMeasurement.strip() == "":
                unitOfMeasurement = None
                dataValue = dataValues[i]
                if dataValue == "AN":
                    dataValue = True
                elif dataValue == "AUS":
                    dataValue = False
            elif unitOfMeasurement == "°C" or unitOfMeasurement == "%":
                dataValue = float(dataValues[i])
            elif unitOfMeasurement == "d" or unitOfMeasurement == "h":
                dataValue = int(dataValues[i])

            data[key] = [dataValue, unitOfMeasurement]

        _LOGGER.debug("Data retrieved from Biostar: %s", data)

        return data

    async def setProgram(self, programID: str) -> bool:
        params = {"syn": "PR001", "value": programID, "key": self._api_key}
        try:
            async with self._session.get(
                f"http://{self._host}/ext/parset.cgi", params=params
            ) as resp:
                status = await resp.json()
            if "ack" in status:
                _LOGGER.debug(
                    f"Biostar heating program successfully set to: {programID}"
                )
                return True
            elif "err" in status:
                _LOGGER.error(
                    f"Biostar heating program not successfully set: {programID}"
                )
                return False

        except:
            _LOGGER.error(
                f"Biostar heating program not successfully set: {status.get('err')}"
            )
            return False


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
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(10):
            currentData = await self.my_api._async_get_data()

        return currentData

    async def setProgram(self, programID: str) -> bool:
        try:
            async with async_timeout.timeout(5):
                result = await self.my_api.setProgram(programID)

            await self.async_refresh()
            return result
        except:
            _LOGGER.error(f"Error changing Biostar heating program to: {programID}")
            return False
