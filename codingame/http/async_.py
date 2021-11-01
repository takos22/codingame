import typing
from http.cookies import Morsel, _quote as cookie_quote

import aiohttp

from .base import BaseHTTPClient
from .httperror import HTTPError

__all__ = ("AsyncHTTPClient",)


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self):
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self.headers
        )

    @property
    def is_async(self):
        return True

    async def close(self):
        await self.__session.close()

    async def request(self, url: str, json: list = []):
        async with self.__session.post(url, json=json) as response:
            data = await response.json()
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError as error:
                raise HTTPError.from_aiohttp(error, data) from None
            return data

    def set_cookie(
        self,
        name: str,
        value: typing.Optional[str] = None,
        domain: str = "www.codingame.com",
    ):
        if value is not None:
            morsel = Morsel()
            morsel.set(name, value, cookie_quote(value))
            morsel["domain"] = domain
            self.__session.cookie_jar.update_cookies({name: morsel})
        else:
            self.__session.cookie_jar._cookies.get(domain, {}).pop(name, None)
