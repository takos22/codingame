import typing
from abc import ABC, abstractmethod

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

__all__ = ("BaseClient",)


class BaseClient(ABC):
    def __init_subclass__(cls, doc_prefix: str = "", **kwargs):
        super().__init_subclass__(**kwargs)

        # Replaces the |maybe_coro| with a new prefix at the start of docstrings

        doc_prefix = doc_prefix.strip() + "\n\n" * (len(doc_prefix) > 0)
        prefix = "|maybe_coro|\n\n"

        for name, method in cls.__dict__.items():
            if not callable(method):
                continue
            if name.startswith("__"):
                continue
            if method.__doc__ is None:  # pragma: no cover
                method.__doc__ = getattr(cls.__base__, name).__doc__

            method.__doc__ = doc_prefix + (
                method.__doc__[len(prefix) :]  # noqa: E203
                if method.__doc__.startswith(prefix)
                else method.__doc__
            )

    def __init__(self, is_async: bool = False):
        self._state = ConnectionState(is_async)

    def __enter__(self):
        if self.is_async:
            raise TypeError(
                "Asynchronous client must be used in an asynchronous "
                "context manager (async with) not in a synchronous one (with)."
            )
        return self

    def __exit__(self, *_):
        self.close()

    async def __aenter__(self):
        if not self.is_async:
            raise TypeError(
                "Synchronous client must be used in a synchronous context"
                "manager (with) not in an asynchronous one (async with)."
            )
        return self

    async def __aexit__(self, *_):
        await self.close()

    def close(self):
        """|maybe_coro|

        Closes the client session.
        """

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
        """Optional :class:`~codingame.CodinGamer`: The CodinGamer that is
        logged in. ``None`` if the client isn't logged in."""
        return self._state.codingamer

    # --------------------------------------------------------------------------
    # CodinGamer

    @abstractmethod
    def login(self, email: str, password: str) -> "CodinGamer":
        """|maybe_coro|

        Login to a CodinGame account.

        Parameters
        -----------
            email: :class:`str`
                Email adress of the account.

            password: :class:`str`
                Password of the account.

        Raises
        ------
            :exc:`~codingame.LoginError`
                Error with the login (empty email, empty password,
                wrong email format, incorrect password, etc).

        Returns
        --------
            :class:`~codingame.CodinGamer`
                The CodinGamer that logged in.
        """

    @abstractmethod
    def get_codingamer(
        self, codingamer: typing.Union[str, int]
    ) -> "CodinGamer":
        """|maybe_coro|

        Get a :class:`~codingame.CodinGamer` from their public handle, their ID
        or from their pseudo.

        .. note::
            ``codingamer`` can be the public handle, the ID or the pseudo.
            Using the public handle or the ID is reccomended because it won't
            change even if the codingamer changes their pseudo.

            The public handle is a 39 character long hexadecimal string that
            is unique to the CodinGamer and identifies them.
            Regex of a public handle: ``[0-9a-f]{32}[0-9]{7}``

            The ID is a 7 number long integer.

        Parameters
        -----------
            codingamer: :class:`str` or :class:`int`
                The CodinGamer's public handle, ID or pseudo.

        Raises
        ------
            :exc:`~codingame.CodinGamerNotFound`
                The CodinGamer with the given public handle, ID or pseudo
                isn't found.

        Returns
        --------
            :class:`~codingame.CodinGamer`
                The requested CodinGamer.
        """

    # --------------------------------------------------------------------------
    # Clash of Code

    @abstractmethod
    def get_clash_of_code(self, handle: str) -> "ClashOfCode":
        """|maybe_coro|

        Get a :class:`Clash of Code <codingame.ClashOfCode>` from its public
        handle.

        Parameters
        -----------
            handle: :class:`str`
                The Clash of Code's public handle. 39 character long hexadecimal
                string (regex: ``[0-9]{7}[0-9a-f]{32}``).

        Raises
        ------
            :exc:`ValueError`
                The Clash of Code handle isn't in the good format.

            :exc:`~codingame.ClashOfCodeNotFound`
                The Clash of Code with the given public handle isn't found.

        Returns
        --------
            :class:`~codingame.ClashOfCode`
                The requested Clash Of Code.
        """

    @abstractmethod
    def get_pending_clash_of_code(self) -> typing.Optional["ClashOfCode"]:
        """|maybe_coro|

        Get the pending public :class:`Clash of Code <codingame.ClashOfCode>`.

        Returns
        --------
            Optional :class:`~codingame.ClashOfCode`
                The pending Clash Of Code if there's one, or ``None`` if there's
                no current public Clash Of Code.
        """

    # --------------------------------------------------------------------------
    # Language IDs

    @abstractmethod
    def get_language_ids(self) -> typing.List[str]:
        """|maybe_coro|

        Get the list of all available language IDs.
        """

    # --------------------------------------------------------------------------
    # Notifications

    @abstractmethod
    def get_unseen_notifications(self) -> typing.Iterator["Notification"]:
        """|maybe_coro|

        Get all the unseen :class:`notifications <codingame.Notification>` of
        the logged in :class:`~codingame.CodinGamer`.

        You need to be logged in to get notifications or else a
        :exc:`~codingame.LoginRequired` will be raised.

        .. note::
            This method is a generator.

        Raises
        ------
            :exc:`~codingame.LoginRequired`
                The Client needs to log in. See :meth:`login`.

        Yields
        -------
            :class:`~codingame.Notification`
                An unseen notification.
        """

    # --------------------------------------------------------------------------
    # Leaderboards

    @abstractmethod
    def get_global_leaderboard(
        self, page: int = 1, type: str = "GENERAL", group: str = "global"
    ) -> "GlobalLeaderboard":
        """|maybe_coro|

        Get the :class:`global leaderboard <codingame.GlobalLeaderboard>` of
        CodinGame.

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

            :exc:`~codingame.LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

        Returns
        --------
            :class:`~codingame.GlobalLeaderboard`
                The global leaderboard of CodinGame.
        """

    @abstractmethod
    def get_challenge_leaderboard(
        self, challenge_id: str, group: str = "global"
    ) -> "ChallengeLeaderboard":
        """|maybe_coro|

        Get the
        :class:`leaderboard of a challenge <codingame.ChallengeLeaderboard>`.

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

            :exc:`~codingame.LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

            :exc:`~codingame.ChallengeNotFound`
                There is no challenge with the given ``challenge_id``.

        Returns
        --------
            :class:`~codingame.ChallengeLeaderboard`
                The leaderboard of the requested challenge.
        """

    @abstractmethod
    def get_puzzle_leaderboard(
        self, puzzle_id: str, group: str = "global"
    ) -> "PuzzleLeaderboard":
        """|maybe_coro|

        Get the :class:`leaderboard of a puzzle <codingame.PuzzleLeaderboard>`.

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

            :exc:`~codingame.LoginRequired`
                The client isn't logged in and the group is one of
                ``"country"``, ``"company"``, ``"school"`` or ``"following"``.

            :exc:`~codingame.PuzzleNotFound`
                There is no puzzle with the given ``puzzle_id``.

        Returns
        --------
            :class:`~codingame.PuzzleLeaderboard`
                The leaderboard of the requested puzzle.
        """
