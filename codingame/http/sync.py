import requests

from .base import BaseHTTPClient
from .httperror import HTTPError

__all__ = ("SyncHTTPClient",)


class SyncHTTPClient(BaseHTTPClient):
    def __init__(self):
        self.__session: requests.Session = requests.Session()

    def close(self):
        self.__session.close()

    def request(self, url: str, json: list = []):
        with self.__session.post(
            url, json=json, headers=self.headers
        ) as response:
            data = response.json()
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                raise HTTPError.from_requests(error, data) from None
            return data
