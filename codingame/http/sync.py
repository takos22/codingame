import typing

import requests

from .base import BaseHTTPClient
from .httperror import HTTPError

__all__ = ("SyncHTTPClient",)


class SyncHTTPClient(BaseHTTPClient):
    def __init__(self):
        self.__session: requests.Session = requests.Session()

    def close(self):
        self.__session.close()

    def request(self, service: str, func: str, parameters: list = []):
        url = self.BASE + service + "/" + func
        with self.__session.post(
            url, json=parameters, headers=self.headers
        ) as response:
            data = response.json()
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                raise HTTPError.from_requests(error, data) from None
            return data

    def set_cookie(
        self,
        name: str,
        value: typing.Optional[str] = None,
        domain: str = "www.codingame.com",
    ):
        return self.__session.cookies.set(name, value, domain=domain)
