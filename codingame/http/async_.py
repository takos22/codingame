import aiohttp

from .base import HTTPClient as BaseHTTPClient
from .httperror import HTTPError


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self):
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession()

    @property
    def is_async(self):
        return True

    async def close(self):
        await self.__session.close()

    async def request(self, url: str, json: list = []):
        with self.__session.post(url, json=json) as response:
            data = await response.json()
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError as error:
                raise HTTPError.from_aiohttp(error, data) from error
            return data
