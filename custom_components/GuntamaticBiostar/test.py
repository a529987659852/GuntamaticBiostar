import asyncio
from distutils.util import strtobool

import aiohttp
from homeassistant.util import slugify


async def main():
    try:
        async with aiohttp.ClientSession("http://192.168.0.34") as session:
            async with session.get("/daqdesc.cgi") as resp:
                assert resp.status == 200
                dataDescription = await resp.text()
                dataDescription = dataDescription.split("\n")[0:-1]
            async with session.get("/daqdata.cgi") as resp:
                assert resp.status == 200
                dataValues = await resp.text()
                dataValues = dataValues.split("\n")[0:-1]
            # print(dataValues)
            data = {}
            for i in range(len(dataDescription)):
                (key, unitOfMeasurement) = dataDescription[i].split(";")
                if key == "reserved":
                    continue
                if unitOfMeasurement.strip() == "":
                    unitOfMeasurement = None
                    dataValue = dataValues[i]
                elif unitOfMeasurement == "°C" or unitOfMeasurement == "%":
                    dataValue = float(dataValues[i])
                elif unitOfMeasurement == "d" or unitOfMeasurement == "h":
                    dataValue = int(dataValues[i])
                data[slugify(key)] = [dataValue, unitOfMeasurement]
    except AssertionError:
        data = {}
    # print(data)

    async with aiohttp.ClientSession("http://192.168.0.34") as session:
        params = {"key": "2261A9253E129CBDB497B755F9962E700879"}
        async with session.get("/ext/daqdesc.cgi", params=params) as resp:
            dataDescription = await resp.json()
            # print(dataDescription)
        async with session.get("/ext/daqdata.cgi", params=params) as resp:
            dataValues = await resp.json()
            # print(dataValues)

        data = {}
        for i in range(len(dataDescription)):
            if dataDescription[i].get("type") == "float":
                print(
                    dataDescription[i].get("name"), type(dataValues[i]), dataValues[i]
                )
            elif dataDescription[i].get("type") == "integer":
                print(
                    dataDescription[i].get("name"), type(dataValues[i]), dataValues[i]
                )
            elif dataDescription[i].get("type") == "boolean":
                print(
                    dataDescription[i].get("name"), type(dataValues[i]), dataValues[i]
                )
            else:
                print(
                    dataDescription[i].get("name"), type(dataValues[i]), dataValues[i]
                )


asyncio.run(main())
