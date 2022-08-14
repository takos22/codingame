import typing
from abc import ABC, abstractmethod
from datetime import datetime

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

    def request(
        self, service: str, func: str, parameters: list = []
    ) -> typing.Any:
        """|maybe_coro|

        Make a request to the CodinGame API service.

        This is useful if you want to use some services that aren't implemented
        yet in this library, but you want to use the authentication that this
        library provides.

        .. note::
            The CodinGame API URLs are in the format
            ``https://www.codingame.com/services/{service}/{func}``.

        Parameters
        -----------
            service: :class:`str`
                The CodinGame API service.

            func: :class:`str`
                The CodinGame API function.

            parameters: Optional :class:`list`
                The parameters to the API.
                Default: ``[]``

        Raises
        ------
            :exc:`ValueError`
                ``service`` or ``function`` parameter is empty.

            :exc:`HTTPError`
                Error with the API (service or function not found, wrong number
                of parameters, bad parameters, etc).

        Returns
        --------
            Anything
                The data returned by the CodinGame API, usually a :class:`dict`.

        .. versionadded:: 1.2
        """

        if service == "":
            raise ValueError("service argument must not be empty.")
        if func == "":
            raise ValueError("func argument must not be empty.")

        return self._state.http.request(service, func, parameters)

    # --------------------------------------------------------------------------
    # CodinGamer

    @abstractmethod
    def login(
        self,
        email: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        remember_me_cookie: typing.Optional[str] = None,
    ) -> typing.Optional["CodinGamer"]:
        """|maybe_coro|

        Login to a CodinGame account.

        .. error::
            As of 2021-10-27, the only way to login is with cookie
            authentication, so with the ``remember_me_cookie`` parameter,
            because of an endpoint change, see :ref:`login`. Using
            email/password authentication will raise a :exc:`LoginError`.

        Parameters
        -----------
            email: Optional :class:`str`
                Email adress of the CodinGamer.
                Not needed if using session ID login.

            password: Optional :class:`str`
                Password of the CodinGamer.
                Not needed if using cookie login.

            remember_me_cookie: Optional :class:`str`
                ``rememberMe`` cookie from CodinGame cookies.
                Not needed if using email/password login.

        Raises
        ------
            :exc:`~codingame.LoginError`
                Error with the login (empty email, empty password,
                wrong email format, incorrect password, etc).

        Returns
        --------
            :class:`~codingame.CodinGamer`
                The CodinGamer that logged in.

        .. versionadded:: 0.3
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

        .. versionadded:: 0.1

        .. versionchanged:: 0.2
            Renamed ``Client.codingamer()`` to
            :meth:`~codingame.Client.get_codingamer`.

        .. versionchanged:: 0.3.3
            Add searching with CodinGamer pseudo.

        .. versionchanged:: 0.3.5
            Add searching with CodinGamer ID.
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
        -------
            :class:`~codingame.ClashOfCode`
                The requested Clash Of Code.

        .. versionadded:: 0.2
        """

    @abstractmethod
    def get_pending_clash_of_code(self) -> typing.Optional["ClashOfCode"]:
        """|maybe_coro|

        Get the pending public :class:`Clash of Code <codingame.ClashOfCode>`.

        Returns
        -------
            Optional :class:`~codingame.ClashOfCode`
                The pending Clash Of Code if there's one, or ``None`` if there's
                no current public Clash Of Code.

        .. versionadded:: 0.3.2
        """

    # --------------------------------------------------------------------------
    # Language IDs

    @abstractmethod
    def get_language_ids(self) -> typing.List[str]:
        """|maybe_coro|

        Get the list of all available language IDs.

        Returns
        -------
            :class:`list` of :class:`int`
                The language IDs.

        .. versionadded:: 0.3

        .. versionchanged:: 1.0
            Renamed ``Client.language_ids`` to
            :meth:`~codingame.Client.get_language_ids`.
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

        .. versionadded:: 0.3.1

        .. versionchanged:: 1.0
            Renamed ``Client.notifications`` to
            :meth:`~codingame.Client.get_unseen_notifications`.
        """

    @abstractmethod
    def get_unread_notifications(self) -> typing.Iterator["Notification"]:
        """|maybe_coro|

        Get all the unread :class:`notifications <codingame.Notification>` of
        the logged in :class:`~codingame.CodinGamer`.

        This includes unseen notifications along with the unread ones.

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
                An unread notification.

        .. versionadded:: 1.3
        """

    @abstractmethod
    def get_read_notifications(self) -> typing.Iterator["Notification"]:
        """|maybe_coro|

        Get the read :class:`notifications <codingame.Notification>` of the
        logged in :class:`~codingame.CodinGamer`.

        You need to be logged in to get notifications or else a
        :exc:`~codingame.LoginRequired` will be raised.

        .. warning::
            There can be some old notifications missing.

        .. note::
            This method is a generator.

        Raises
        ------
            :exc:`~codingame.LoginRequired`
                The Client needs to log in. See :meth:`login`.

        Yields
        -------
            :class:`~codingame.Notification`
                A read notification.

        .. versionadded:: 1.3
        """

    @abstractmethod
    def mark_notifications_as_seen(
        self, notifications: typing.List[typing.Union["Notification", int]]
    ) -> datetime:
        """|maybe_coro|

        Mark :class:`notifications <codingame.Notification>` of the
        logged in :class:`~codingame.CodinGamer` as seen.

        You need to be logged in to mark notifications as seen or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            notifications: :class:`list` of :class:`~codingame.Notification` or\
            :class:`int`
                The notifications to mark as seen. Can be either the
                notification or its ID.

        Raises
        ------
            :exc:`~codingame.LoginRequired`
                The Client needs to log in. See :meth:`login`.

            :exc:`ValueError`
                `notifications` parameter is empty.

        Returns
        -------
            :class:`~datetime.datetime`
                The time when this notification was marked as seen.

        .. versionadded:: 1.4
        """

    @abstractmethod
    def mark_notifications_as_read(
        self, notifications: typing.List[typing.Union["Notification", int]]
    ) -> datetime:
        """|maybe_coro|

        Mark :class:`notifications <codingame.Notification>` of the
        logged in :class:`~codingame.CodinGamer` as read.

        You need to be logged in to mark notifications as read or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            notifications: :class:`list` of :class:`~codingame.Notification` or\
            :class:`int`
                The notifications to mark as read. Can be either the
                notification or its ID.

        Raises
        ------
            :exc:`~codingame.LoginRequired`
                The Client needs to log in. See :meth:`login`.

            :exc:`ValueError`
                `notifications` parameter is empty.

        Returns
        -------
            :class:`~datetime.datetime`
                The time when this notification was marked as read.

        .. versionadded:: 1.4
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

        .. versionadded:: 0.4
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

        .. versionadded:: 0.4
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

        .. versionadded:: 0.4
        """
