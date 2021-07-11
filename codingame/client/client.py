from .base import BaseClient

__all__ = ("Client",)


class Client(BaseClient):
    """Client for the CodinGame API.

    Instanciates a :class:`~codingame.client.sync.SyncClient` if ``is_async`` is
    ``False`` or not given.
    Instanciates a :class:`~codingame.client.async_.AsyncClient` if ``is_async``
    is ``True``.

    Parameters
    ----------
        is_async : bool
            Whether the client is asynchronous. Defaults to ``False``.
    """

    def __new__(cls, is_async: bool = False):
        if is_async:
            from .async_ import AsyncClient

            return AsyncClient()
        else:
            from .sync import SyncClient

            return SyncClient()
