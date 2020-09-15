import requests

from .endpoints import Endpoints
from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode
from .exceptions import CodinGamerNotFound, ClashOfCodeNotFound


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

    def get_clash_of_code(self, clash_of_code_handle: str) -> ClashOfCode:
        """Get a Clash of Code from its public handle.

        Parameters
        -----------
            clash_of_code_handle: :class:`str`
                The Clash of Code's public handle (39 character long hexadecimal string).

        Raises
        ------
            :exc:`.ClashOfCodeNotFound`
                The Clash of Code with the given public handle isn't found.

        Returns
        --------
            :class:`ClashOfCode`
                The ClashOfCode.
        """

        r = self._session.post(Endpoints.ClashOfCode, json=[clash_of_code_handle])
        if r.json() is None:
            raise ClashOfCodeNotFound(f"No CodinGamer with handle {clash_of_code_handle!r}")
        return ClashOfCode(session=self._session, **r.json())
