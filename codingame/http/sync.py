import requests

from .base import HTTPClient as BaseHTTPClient
from .httperror import HTTPError

class SyncHTTPClient(BaseHTTPClient):
    def __init__(self):
        self.__session: requests.Session = requests.Session()

    def close(self):
        self.__session.close()

    def request(self, url: str, json: list = []):
        with self.__session.post(url, json=json) as response:
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                raise HTTPError.from_aiohttp(error) from error
            return response.json()
