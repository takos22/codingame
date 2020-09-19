import requests
import re

from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode
from .endpoints import Endpoints
from .exceptions import CodinGamerNotFound, ClashOfCodeNotFound
from .utils import validate_args


class Client:
    """CodinGame API client."""

    _CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
    _CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")

    def __init__(self):
        self._session = requests.Session()

    @validate_args
    def get_codingamer(self, codingamer_handle: str) -> CodinGamer:
        """Get a CodinGamer from his public handle.

        Parameters
        -----------
            codingamer_handle: :class:`str`
                The CodinGamer's public handle.
                39 character long hexadecimal string (regex: ``[0-9a-f]{32}[0-9]{7}``).

        Raises
        ------
            :exc:`ValueError`
                The CodinGamer handle isn't in the good format.

            :exc:`.CodinGamerNotFound`
                The CodinGamer with the given public handle isn't found.

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer.
        """

        if not self._CODINGAMER_HANDLE_REGEX.match(codingamer_handle):
            raise ValueError(
                f"CodinGamer handle {codingamer_handle!r} isn't in the good format "
                "(regex: [0-9a-f]{{32}}[0-9]{{7}})."
            )

        r = self._session.post(Endpoints.CodinGamer, json=[codingamer_handle])
        if r.json() is None:
            raise CodinGamerNotFound(f"No CodinGamer with handle {codingamer_handle!r}")
        return CodinGamer(client=self, **r.json()["codingamer"])

    @validate_args
    def get_clash_of_code(self, clash_of_code_handle: str) -> ClashOfCode:
        """Get a Clash of Code from its public handle.

        Parameters
        -----------
            clash_of_code_handle: :class:`str`
                The Clash of Code's public handle.
                39 character long hexadecimal string (regex: ``[0-9]{7}[0-9a-f]{32}``).

        Raises
        ------
            :exc:`ValueError`
                The Clash of Code handle isn't in the good format.

            :exc:`.ClashOfCodeNotFound`
                The Clash of Code with the given public handle isn't found.

        Returns
        --------
            :class:`ClashOfCode`
                The ClashOfCode.
        """

        if not self._CLASH_OF_CODE_HANDLE_REGEX.match(clash_of_code_handle):
            raise ValueError(
                f"CodinGamer handle {clash_of_code_handle!r} isn't in the good format "
                "(regex: [0-9]{{7}}[0-9a-f]{{32}})."
            )

        r = self._session.post(Endpoints.ClashOfCode, json=[clash_of_code_handle])
        if r.json() is None:
            raise ClashOfCodeNotFound(f"No CodinGamer with handle {clash_of_code_handle!r}")
        return ClashOfCode(client=self, **r.json())
