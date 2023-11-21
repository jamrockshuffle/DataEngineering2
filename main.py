import os
import urllib
import zipfile
import aiohttp
import asyncio
import nest_asyncio
import requests

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


async def async_download():
    async with aiohttp.ClientSession() as session:
        for x in download_uris:
            split = urllib.parse.urlsplit(x)
            filename = split.path.split("/")[-1]
            async with session.get(x) as resp:
                if resp.status == 200:
                    with open("Downloads_PY/" + filename, 'wb') as file:
                        async for chunk in resp.content.iter_chunked(10):
                            file.write(chunk)


def main():
    if not os.path.exists("Downloads_PY"):
        os.mkdir("Downloads_PY")

    for i in download_uris:
        split = urllib.parse.urlsplit(i)
        filename = split.path.split("/")[-1]
        try:
            response = urllib.request.urlretrieve(i, "Downloads_PY/" + filename)
        except:
            continue

        with zipfile.ZipFile("Downloads_PY/" + filename, 'r') as zip:
            zip.extractall("Downloads_PY")

        os.remove("Downloads_PY/" + filename)

    pass


if __name__ == "__main__":
    main()
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_download())
