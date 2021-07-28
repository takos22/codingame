import typing

import aiohttp

from .base import BaseHTTPClient
from .httperror import HTTPError

if typing.TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("AsyncHTTPClient",)


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self, state: "ConnectionState"):
        self.state = state
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self.headers
        )

    @property
    def is_async(self):
        return True

    async def close(self):
        await self.__session.close()

    async def request(self, service: str, func: str, json: list = []):
        url = self.BASE + service + "/" + func
        async with self.__session.post(url, json=json) as response:
            data = await response.json()
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError as error:
                raise HTTPError.from_aiohttp(error, data) from None
            return data
