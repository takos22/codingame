import typing

from .http import HTTPClient

if typing.TYPE_CHECKING:
    from .codingamer import CodinGamer

__all__ = ("ConnectionState",)


class ConnectionState:
    """Saves information about the state of the connection to the API."""

    http: "HTTPClient"
    logged_in: bool
    codingamer: typing.Optional["CodinGamer"]

    def __init__(self, is_async: bool = False):
        self.http = HTTPClient(self, is_async)

        self.logged_in = False
        self.codingamer = None

    @property
    def is_async(self) -> bool:
        "Whether the HTTP client is async."
        return self.http.is_async
