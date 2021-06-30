import typing
from abc import ABC, abstractmethod

from ..http import HTTPClient
from ..state import ConnectionState

if typing.TYPE_CHECKING:
    from ..clash_of_code import ClashOfCode
    from ..codingamer import CodinGamer
    from ..leaderboard import (
        ChallengeLeaderboard,
        GlobalLeaderboard,
        PuzzleLeaderboard,
    )
    from ..notification import Notification


class BaseClient(ABC):
    def __init__(self, is_async: bool = False):
        http_client = HTTPClient(is_async=is_async)
        self._state = ConnectionState(http_client)

    def close(self):
        self._state.http.close()

    @property
    def is_async(self) -> bool:
        """:class:`bool`: Whether the client is asynchronous."""
        return self._state.is_async

    @property
    def logged_in(self) -> bool:
        """:class:`bool`: Whether the client is logged in."""
        return self._state.logged_in

    @property
    def codingamer(self) -> typing.Optional["CodinGamer"]:
        """Optional :class:`CodinGamer`: The CodinGamer that is logged in.
        ``None`` if the client isn't logged in."""
        return self._state.codingamer

    @abstractmethod
    def login(self, email: str, password: str) -> "CodinGamer":
        """Login to a CodinGamer account.

        Parameters
        -----------
            email: :class:`str`
                Email adress of the CodinGamer.

            password: :class:`str`
                Password of the CodinGamer.

        Raises
        ------
            :exc:`LoginError`
                Error with the login (empty email, empty password,
                wrong email format, incorrect password, etc).

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer that logged in.
        """

    @abstractmethod
    def get_codingamer(
        self, codingamer: typing.Union[str, int]
    ) -> "CodinGamer":
        """Get a CodinGamer from their public handle, their ID or from their
        username.

        .. note::
            ``codingamer`` can be the public handle, the id or the username.
            Using the public handle or the ID is reccomended because it won't
            change even if the codingamer changes their username.

            The public handle is a 39 character long hexadecimal string that
            represents the user.
            Regex of a public handle: ``[0-9a-f]{32}[0-9]{7}``

            The ID is a 7 number long integer.

        Parameters
        -----------
            codingamer: :class:`str` or :class:`int`
                The CodinGamer's public handle, ID or username.

        Raises
        ------
            :exc:`CodinGamerNotFound`
                The CodinGamer with the given public handle, ID or username
                isn't found.

        Returns
        --------
            :class:`CodinGamer`
                The CodinGamer.
        """

    @abstractmethod
    def get_clash_of_code(self, handle: str) -> "ClashOfCode":
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

            :exc:`ClashOfCodeNotFound`
                The Clash of Code with the given public handle isn't found.

        Returns
        --------
            :class:`ClashOfCode`
                The ClashOfCode.
        """

    @abstractmethod
    def get_pending_clash_of_code(self) -> typing.Optional["ClashOfCode"]:
        """Get a pending Clash of Code.

        Returns
        --------
            Optional :class:`ClashOfCode`
                The pending ClashOfCode if there's one or ``None``.
        """

    @abstractmethod
    def get_language_ids(self) -> typing.List[str]:
        """Get the list of all available language ids."""

    @abstractmethod
    def get_unseen_notifications(self) -> typing.Iterator["Notification"]:
        """Get all the unseen notifications of the logged in CodinGamer.

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
                A Notification.
        """

    @abstractmethod
    def get_global_leaderboard(
        self, page: int = 1, type: str = "GENERAL", group: str = "global"
    ) -> "GlobalLeaderboard":
        """Get the global leaderboard in CodinGame.

        You can specify an optional page, type of leaderboard and the group of
        users to rank.

        Parameters
        -----------
            page: Optional :class:`int`
                The page of the leaderboard to get the users from.
                Default: ``1``.

            type: Optional :class:`str`
                The type of global leaderboard to show.
                One of ``"GENERAL"``, ``"CONTESTS"``, ``"BOT_PROGRAMMING"``,
                ``"OPTIM"`` or ``"CODEGOLF"``.
                Default: ``"GENERAL"``.

            group: Optional :class:`str`
                The group of users to rank. For every group except ``"global"``,
                you need to be logged in.
                One of ``"global"``, ``"country"``, ``"company"``, ``"school"``
                or ``"following"``.
                Default: ``"global"``.

        Raises
        ------
            :exc:`ValueError`
                One of the arguments isn't one of the accepted arguments.

            :exc:`LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

        Returns
        --------
            :class:`GlobalLeaderboard`
                The global leaderboard.
        """

    @abstractmethod
    def get_challenge_leaderboard(
        self, challenge_id: str, group: str = "global"
    ) -> "ChallengeLeaderboard":
        """Get the leaderboard of a challenge.

        You can specify an optional group of users to rank.

        Parameters
        -----------
            challenge_id: :class:`str`
                The string that identifies the challenge.

            group: Optional :class:`str`
                The group of users to rank. For every group except ``"global"``,
                you need to be logged in.
                One of ``"global"``, ``"country"``, ``"company"``, ``"school"``
                or ``"following"``.
                Default: ``"global"``.

        Raises
        ------
            :exc:`ValueError`
                One of the arguments isn't one of the accepted arguments.

            :exc:`LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

            :exc:`ChallengeNotFound`
                There is no challenge with the given challenge_id.

        Returns
        --------
            :class:`ChallengeLeaderboard`
                The challenge leaderboard.
        """

    @abstractmethod
    def get_puzzle_leaderboard(
        self, puzzle_id: str, group: str = "global"
    ) -> "PuzzleLeaderboard":
        """Get the leaderboard of a puzzle.

        You can specify an optional group of users to rank.

        Parameters
        -----------
            puzzle_id: :class:`str`
                The string that identifies the puzzle.

            group: Optional :class:`str`
                The group of users to rank. For every group except ``"global"``,
                you need to be logged in.
                One of ``"global"``, ``"country"``, ``"company"``, ``"school"``
                or ``"following"``.
                Default: ``"global"``.

        Raises
        ------
            :exc:`ValueError`
                One of the arguments isn't one of the accepted arguments.

            :exc:`LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

            :exc:`PuzzleNotFound`
                There is no puzzle with the given puzzle_id.

        Returns
        --------
            :class:`PuzzleLeaderboard`
                The puzzle leaderboard.
        """