import requests
import re

from typing import List, Optional, Iterator

from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode
from .notification import Notification

from .endpoints import Endpoints
from .exceptions import CodinGamerNotFound, ClashOfCodeNotFound, LoginRequired
from .utils import validate_args


class Client:
    """CodinGame API client.

    Attributes
    -----------
        logged_in: :class:`bool`
            If the client is logged in as a CodinGamer.

        codingamer: Optional[:class:`CodinGamer`]
            The CodinGamer that is logged in through the client. ``None`` if the client isn't logged in.
    """

    _CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
    _CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")

    logged_in: bool
    codingamer: Optional[CodinGamer]

    def __init__(self, email: str = None, password: str = None):
        self._session = requests.Session()

        self.logged_in = False
        self.codingamer = None
        if email is not None and password is not None:
            self.login(email, password)

    @validate_args
    def login(self, email: str, password: str):
        """Login to a CodinGamer account.

        Parameters
        -----------
            email: :class:`str`
                Email adress of the CodinGamer.

            password: :class:`str`
                Password of the CodinGamer.

        Raises
        ------
            :exc:`ValueError`
                Error with the login (empty email, empty password, wrong email format, incorrect password, etc).

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer that is logged in.
        """

        if email == "":
            raise ValueError("Email is required")
        if password == "":
            raise ValueError("Password is required")

        r = self._session.post(Endpoints.CodinGamer_login, json=[email, password, True])
        json = r.json()
        if "id" in json and "message" in json:
            raise ValueError(f"{json['id']}: {json['message']}")
        self.logged_in = True
        self.codingamer = CodinGamer(client=self, **json["codinGamer"])
        return self.codingamer

    @validate_args
    def get_codingamer(self, codingamer) -> CodinGamer:
        """Get a CodinGamer from their public handle or from their username.

        .. note::
            ``codingamer`` can be the public handle or the username. Using the public handle
            is reccomended because it won't change even if the codingamer changes their username.

            The public handle is a 39 character long hexadecimal string that represents the user.
            Regex of a public handle: ``[0-9a-f]{32}[0-9]{7}``

        Parameters
        -----------
            codingamer: :class:`str`
                The CodinGamer's public handle or username.

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

        if not self._CODINGAMER_HANDLE_REGEX.match(codingamer):
            r = self._session.post(Endpoints.Search, json=[codingamer, "en", None])
            search: List[dict] = r.json()
            users = [query for query in search if query["type"] == "USER"]
            if users:
                handle = users[0]["id"]
            else:
                raise CodinGamerNotFound(f"No CodinGamer with username {codingamer!r}")
        else:
            handle = codingamer

        r = self._session.post(Endpoints.CodinGamer, json=[handle])
        json = r.json()
        if json is None:
            raise CodinGamerNotFound(f"No CodinGamer with handle {handle!r}")
        return CodinGamer(client=self, **json["codingamer"])

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
                f"Clash of Code handle {clash_of_code_handle!r} isn't in the good format "
                "(regex: [0-9]{7}[0-9a-f]{32})."
            )

        r = self._session.post(Endpoints.ClashOfCode, json=[clash_of_code_handle])
        json = r.json()
        if "id" in json and "message" in json:
            raise ClashOfCodeNotFound(f"No Clash of Code with handle {clash_of_code_handle!r}")
        return ClashOfCode(client=self, **json)

    def get_pending_clash_of_code(self) -> Optional[ClashOfCode]:
        """Get a pending Clash of Code.

        Returns
        --------
            Optional[:class:`ClashOfCode`]
                The pending ClashOfCode if there's one or ``None``.
        """

        r = self._session.post(Endpoints.ClashOfCode_pending, json=[])
        json = r.json()
        if len(json) == 0:
            return None
        return ClashOfCode(client=self, **json[0])

    @property
    def language_ids(self) -> List[str]:
        """List[:class:`str`]: List of all available language ids."""

        if hasattr(self, "_language_ids"):
            return self._language_ids
        else:
            r = self._session.post(Endpoints.LanguageIds, json=[])
            self._language_ids = r.json()
            return self._language_ids

    @property
    def notifications(self) -> Iterator[Notification]:
        """Get all the unseen notifications of the Client.

        You need to be logged in to get notifications or else a :exc:`LoginRequired` will be raised.

        .. note::
            This property is a generator.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`login`.

        Yields
        -------
            :class:`Notification`
                The Notification.
        """

        if not self.logged_in:
            raise LoginRequired()

        r = self._session.post(Endpoints.UnseenNotifications, json=[self.codingamer.id])
        for notification in r.json():
            yield Notification(notification)
