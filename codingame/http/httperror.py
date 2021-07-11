import typing

if typing.TYPE_CHECKING:
    import aiohttp
    import requests


__all__ = ("HTTPError",)


class HTTPError(Exception):
    def __init__(self, status_code: int, reason: str, data):
        self.status_code: int = status_code
        self.reason: str = reason
        self.data = data

    def __str__(self):
        return f"HTTPError: {self.status_code}: {self.reason}, {self.data!r}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.status_code}, {self.reason!r})"

    @classmethod
    def from_requests(
        cls, http_error: "requests.HTTPError", data
    ) -> "HTTPError":
        status_code = http_error.response.status_code
        reason = http_error.response.reason
        return cls(status_code, reason, data)

    @classmethod
    def from_aiohttp(
        cls, http_error: "aiohttp.ClientResponseError", data
    ) -> "HTTPError":  # pragma: no cover
        status_code = http_error.status
        reason = http_error.message
        return cls(status_code, reason, data)
