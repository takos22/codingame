import requests

from typing import Optional

from .endpoints import Endpoints
from .codingamer import CodinGamer
from .exceptions import CodinGamerNotFound


class Client:
    """CodinGame API client."""

    def __init__(self):
        self._session = requests.Session()

    def codingamer(self, codingamer_handle: str) -> Optional[CodinGamer]:
        """Get a CodinGamer from his public handle."""

        r = self._session.post(Endpoints.CodinGamer, json=[codingamer_handle])
        if r.json() is None:
            raise CodinGamerNotFound(f"No CodinGamer with handle {repr(codingamer_handle)}")
        return CodinGamer(**r.json()["codingamer"])
