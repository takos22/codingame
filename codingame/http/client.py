from .base import BaseHTTPClient


class HTTPClient(BaseHTTPClient):
    def __new__(cls, is_async: bool = False):
        if is_async:
            from .async_ import AsyncHTTPClient

            return AsyncHTTPClient()
        else:
            from .sync import SyncHTTPClient

            return SyncHTTPClient()