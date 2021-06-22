import re
import typing

from .clash_of_code import ClashOfCode
from .codingamer import CodinGamer
from .exceptions import (
    ClashOfCodeNotFound,
    CodinGamerNotFound,
    LoginError,
    LoginRequired,
)
from .http import HTTPError, SyncHTTPClient
from .leaderboard import (
    ChallengeLeaderboard,
    GlobalLeaderboard,
    PuzzleLeaderboard,
)
from .notification import Notification
from .state import ConnectionState

_CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
_CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")


class Client:
    """CodinGame API client.

    Attributes
    -----------
        logged_in: :class:`bool`
            If the client is logged in as a CodinGamer.

        codingamer: Optional[:class:`CodinGamer`]
            The CodinGamer that is logged in through the client.
            ``None`` if the client isn't logged in.
    """

    def __init__(self, is_async: bool = False):
        if is_async:
            raise NotImplementedError("Async client isn't ready to be used yet")
            # http_client = AsyncHTTPClient()
        else:
            http_client = SyncHTTPClient()

        self._state = ConnectionState(http_client)

    def close(self):
        self._state.http.close()

    @property
    def is_async(self) -> bool:
        "Whether the client is async."
        return self._state.is_async

    @property
    def logged_in(self) -> bool:
        return self._state.logged_in

    @property
    def codingamer(self) -> typing.Optional[CodinGamer]:
        return self._state.codingamer

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
                Error with the login (empty email, empty password,
                wrong email format, incorrect password, etc).

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer that is logged in.
        """

        try:
            data = self._state.http.login(email, password)
        except HTTPError as error:
            raise LoginError.from_id(error.data["id"], error.data["message"])

        self._state.logged_in = True
        self._state.codingamer = CodinGamer(self._state, data["codinGamer"])
        return self.codingamer

    def get_codingamer(self, codingamer) -> CodinGamer:
        """Get a CodinGamer from their public handle, their id or from their
        username.

        .. note::
            ``codingamer`` can be the public handle, the id or the username.
            Using the public handle or the id is reccomended because it won't
            change even if the codingamer changes their username.

            The public handle is a 39 character long hexadecimal string that
            represents the user.
            Regex of a public handle: ``[0-9a-f]{32}[0-9]{7}``

            The id is a 7 number long integer.

        Parameters
        -----------
            codingamer: :class:`str`
                The CodinGamer's public handle, id or username.

        Raises
        ------
            :exc:`.CodinGamerNotFound`
                The CodinGamer with the given public handle, id or username
                isn't found.

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer.
        """

        handle = None

        if isinstance(codingamer, int):
            try:
                data = self._state.http.get_codingamer_from_id(codingamer)
            except HTTPError as error:
                if error.data["id"] == 404:
                    raise CodinGamerNotFound(
                        f"No CodinGamer with id {codingamer!r}"
                    )
                raise  # pragma: no cover
            handle = data["publicHandle"]

        if handle is None and not _CODINGAMER_HANDLE_REGEX.match(codingamer):
            results = self._state.http.search(codingamer)
            users = [result for result in results if result["type"] == "USER"]
            if users:
                handle = users[0]["id"]
            else:
                raise CodinGamerNotFound(
                    f"No CodinGamer with username {codingamer!r}"
                )
        elif handle is None:
            handle = codingamer

        data = self._state.http.get_codingamer_from_handle(handle)
        if data is None:
            raise CodinGamerNotFound(f"No CodinGamer with handle {handle!r}")
        return CodinGamer(self._state, data["codingamer"])

    def get_clash_of_code(self, handle: str) -> ClashOfCode:
        """Get a Clash of Code from its public handle.

        Parameters
        -----------
            handle: :class:`str`
                The Clash of Code's public handle. 39 character long hexadecimal
                string (regex: ``[0-9]{7}[0-9a-f]{32}``).

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

        if not _CLASH_OF_CODE_HANDLE_REGEX.match(handle):
            raise ValueError(
                f"Clash of Code handle {handle!r} isn't in the good format "
                "(regex: [0-9]{7}[0-9a-f]{32})."
            )

        try:
            data = self._state.http.get_clash_of_code_from_handle(handle)
        except HTTPError as error:
            if error.data["id"] == 502:
                raise ClashOfCodeNotFound(
                    f"No Clash of Code with handle {handle!r}"
                )
            raise  # pragma: no cover
        return ClashOfCode(self._state, data)

    def get_pending_clash_of_code(self) -> typing.Optional[ClashOfCode]:
        """Get a pending Clash of Code.

        Returns
        --------
            Optional[:class:`ClashOfCode`]
                The pending ClashOfCode if there's one or ``None``.
        """

        data: list = self._state.http.get_pending_clash_of_code()
        if len(data) == 0:
            return None  # pragma: no cover
        return ClashOfCode(self._state, data[0])  # pragma: no cover

    def get_language_ids(self) -> typing.List[str]:
        """Get the list of all available language ids."""

        return self._state.http.get_language_ids()

    def get_unseen_notifications(self) -> typing.Iterator[Notification]:
        """Get all the unseen notifications of the Client.

        You need to be logged in to get notifications or else a
        :exc:`LoginRequired` will be raised.

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

        data = self._state.http.get_unseen_notifications(self.codingamer.id)
        for notification in data:
            yield Notification(self._state, notification)

    def get_global_leaderboard(
        self, page: int = 1, type: str = "GENERAL", group: str = "global"
    ) -> GlobalLeaderboard:
        type = type.upper()
        if type not in [
            "GENERAL",
            "CONTESTS",
            "BOT_PROGRAMMING",
            "OPTIM",
            "CODEGOLF",
        ]:
            raise ValueError(
                "type argument must be one of: GENERAL, CONTESTS, "
                f"BOT_PROGRAMMING, OPTIM, CODEGOLF. Got: {type}"
            )

        group = group.lower()
        if group not in [
            "global",
            "country",
            "company",
            "school",
            "following",
        ]:
            raise ValueError(
                "group argument must be one of: global, country, company, "
                f"school, following. Got: {group}"
            )

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise LoginRequired()

        data = self._state.http.get_global_leaderboard(
            page,
            type,
            group,
            self.codingamer.public_handle if self.logged_in else "",
        )
        return GlobalLeaderboard(self._state, type, group, page, data)

    def get_challenge_leaderboard(
        self, challenge_id: str, group: str = "global"
    ) -> ChallengeLeaderboard:
        group = group.lower()
        if group not in [
            "global",
            "country",
            "company",
            "school",
            "following",
        ]:
            raise ValueError(
                "group argument must be one of: global, country, company, "
                f"school, following. Got: {group}"
            )

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise LoginRequired()

        data = self._state.http.get_challenge_leaderboard(
            challenge_id,
            group,
            self.codingamer.public_handle if self.logged_in else "",
        )
        return ChallengeLeaderboard(self._state, challenge_id, group, data)

    def get_puzzle_leaderboard(
        self, puzzle_id: str, group: str = "global"
    ) -> PuzzleLeaderboard:
        group = group.lower()
        if group not in [
            "global",
            "country",
            "company",
            "school",
            "following",
        ]:
            raise ValueError(
                "group argument must be one of: global, country, company, "
                f"school, following. Got: {group}"
            )

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise LoginRequired()

        data = self._state.http.get_puzzle_leaderboard(
            puzzle_id,
            group,
            self.codingamer.public_handle if self.logged_in else "",
        )
        return PuzzleLeaderboard(self._state, puzzle_id, group, data)
