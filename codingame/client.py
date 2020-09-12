import requests

from typing import Optional

from .endpoints import Endpoints
from .codingamer import CodinGamer
from .exceptions import CodinGamerNotFound


class Client:
    """CodinGame API client."""

    def __init__(self):
        self._session = requests.Session()

    def get_codingamer(self, codingamer_handle: str) -> CodinGamer:
        """Get a CodinGamer from his public handle.

        Parameters
        -----------
        codingamer_handle: :class:`str`
            The CodinGamer's public handle (39 character long hexadecimal string).

        Raises
        ------
        :exc:`.CodinGamerNotFound`
            The CodinGamer with the given public handle isn't found.

        Returns
        --------
        :class:`CodinGamer`
            The CodinGamer.
        """

        r = self._session.post(Endpoints.CodinGamer, json=[codingamer_handle])
        if r.json() is None:
            raise CodinGamerNotFound(f"No CodinGamer with handle {codingamer_handle!r}")
        return CodinGamer(**r.json()["codingamer"])
