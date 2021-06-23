from .async_ import AsyncClient
from .base import BaseClient
from .sync import SyncClient


class Client(BaseClient):
    def __new__(cls, is_async: bool = False):
        if is_async:
            raise NotImplementedError("Async client isn't ready to be used yet")
            # return AsyncClient()
        else:
            return SyncClient()
