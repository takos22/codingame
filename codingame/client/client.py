from .base import BaseClient


class Client(BaseClient):
    def __new__(cls, is_async: bool = False):
        if is_async:
            from .async_ import AsyncClient

            return AsyncClient()
        else:
            from .sync import SyncClient

            return SyncClient()
