import typing

from .base import BaseHTTPClient

if typing.TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("HTTPClient",)


class HTTPClient(BaseHTTPClient):
    def __new__(cls, state: "ConnectionState", is_async: bool = False):
        if is_async:
            from .async_ import AsyncHTTPClient

            return AsyncHTTPClient(state)
        else:
            from .sync import SyncHTTPClient

            return SyncHTTPClient(state)
