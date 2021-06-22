import typing

if typing.TYPE_CHECKING:
    from .codingamer import CodinGamer
    from .http.base import HTTPClient


class ConnectionState:

    logged_in: bool
    codingamer: typing.Optional["CodinGamer"]

    """Saves information about the state of the connection to the API."""

    def __init__(self, http_client: "HTTPClient"):
        self.http = http_client

        self.logged_in = False
        self.codingamer = None

    @property
    def is_async(self) -> bool:
        "Whether the HTTP client is async."
        return self.http.is_async