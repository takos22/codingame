from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, Optional

from .abc import BaseObject, BaseUser
from .exceptions import ClashOfCodeError, LoginRequired
from .http.httperror import HTTPError
from .types.clash_of_code import ClashOfCode as ClashOfCodeDict
from .types.clash_of_code import (
    LanguageId,
    LanguageIds,
    Mode,
    Modes,
    PlayerStatus,
)
from .utils import minified_players_to_players, to_datetime

if TYPE_CHECKING:
    from .state import ConnectionState

__all__ = (
    "ClashOfCode",
    "Player",
)


class ClashOfCode(BaseObject):
    """Represents a Clash of Code.

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the Clash of Code (hexadecimal str).

        join_url: :class:`str`
            URL to join the Clash of Code.

        public: :class:`bool`
            Whether the Clash of Code is public.

        min_players: :class:`int`
            Minimum number of players.

        max_players: :class:`int`
            Maximum number of players.

        modes: Optional :class:`list` of :class:`str`
            List of possible modes.

        programming_languages: Optional :class:`list` of :class:`str`
            List of possible programming languages.

        started: :class:`bool`
            Whether the Clash of Code is started.

        finished: :class:`bool`
            Whether the Clash of Code is finished.

        mode: Optional :class:`str`
            The mode of the Clash of Code.

        creation_time: :class:`~datetime.datetime`
            Creation time of the Clash of Code.

        start_time: :class:`~datetime.datetime`
            Start time of the Clash of Code. If the Clash of Code hasn't started
            yet, this is the expected start time of the Clash of Code.

        end_time: Optional :class:`~datetime.datetime`
            End time of the Clash of Code.

        time_before_start: :class:`~datetime.timedelta`
            Time before the start of the Clash of Code.

        time_before_end: Optional :class:`~datetime.timedelta`
            Time before the end of the Clash of Code.

        players: :class:`list` of :class:`Player`
            List of the players in the Clash of Code.
    """

    public_handle: str
    join_url: str
    public: bool
    min_players: int
    max_players: int
    modes: Optional[Modes]
    programming_languages: Optional[LanguageIds]
    started: bool
    finished: bool
    mode: Optional[Mode]
    creation_time: datetime
    start_time: datetime
    end_time: Optional[datetime]
    time_before_start: timedelta
    time_before_end: Optional[timedelta]
    players: List["Player"]

    __slots__ = (
        "public_handle",
        "join_url",
        "public",
        "min_players",
        "max_players",
        "modes",
        "programming_languages",
        "started",
        "finished",
        "mode",
        "creation_time",
        "start_time",
        "end_time",
        "time_before_start",
        "time_before_end",
        "players",
    )

    def __init__(self, state: "ConnectionState", data: ClashOfCodeDict):
        super().__init__(state)
        self._set_data(data)

    def _set_data(self, data: ClashOfCodeDict):
        self._setattr("public_handle", data["publicHandle"])
        self._setattr(
            "join_url",
            f"https://www.codingame.com/clashofcode/clash/{self.public_handle}",
        )

        self._setattr("public", data["publicClash"])
        self._setattr("min_players", data["nbPlayersMin"])
        self._setattr("max_players", data["nbPlayersMax"])
        self._setattr("modes", data.get("modes"))
        self._setattr("programming_languages", data.get("programmingLanguages"))

        self._setattr("started", data["started"])
        self._setattr("finished", data["finished"])
        self._setattr("mode", data.get("mode"))

        self._setattr("creation_time", to_datetime(data["creationTime"]))
        self._setattr("start_time", to_datetime(data.get("startTime")))
        self._setattr("end_time", to_datetime(data.get("endTime")))

        self._setattr(
            "time_before_start", timedelta(milliseconds=data["msBeforeStart"])
        )
        self._setattr(
            "time_before_end",
            timedelta(milliseconds=data["msBeforeEnd"])
            if "msBeforeEnd" in data
            else None,
        )

        self._setattr(
            "players",
            [
                Player(
                    self._state,
                    self,
                    self.started,
                    self.finished,
                    player,
                )
                for player in data.get("players", [])
            ]
            or minified_players_to_players(data.get("minifiedPlayers", [])),
        )

    def __repr__(self) -> str:
        return (
            "<ClashOfCode public_handle={0.public_handle!r} "
            "public={0.public!r} modes={0.modes!r} "
            "programming_languages={0.programming_languages!r} "
            "started={0.started!r} finished={0.finished!r} "
            "players={0.players!r}>".format(self)
        )


    def fetch(self):
        """|maybe_coro|

        Get and update the information about this Clash Of Code.
        """

        if self._state.is_async:

            async def _fetch():
                data = await self._state.http.get_clash_of_code_from_handle(
                    self.public_handle
                )
                self._set_data(data)

        else:

            def _fetch():
                data = self._state.http.get_clash_of_code_from_handle(
                    self.public_handle
                )
                self._set_data(data)

        return _fetch()

    def join(self):
        """|maybe_coro|

        Join this Clash Of Code.

        You need to be logged in to join a Clash of Code or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _join():
                try:
                    data = await self._state.http.join_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        else:

            def _join():
                try:
                    data = self._state.http.join_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        return _join()

    def start(self):
        """|maybe_coro|

        Start this Clash Of Code.

        You need to be logged in as the owner to start a Clash of Code or else a
        :exc:`~codingame.LoginRequired` will be raised.

        .. note::
            This sets the countdown to the start to 5s. You will need to fetch
            the Clash Of Code again in 5-10s.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _start():
                try:
                    await self._state.http.start_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                    data = await self._state.http.get_clash_of_code_from_handle(
                        self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        else:

            def _start():
                try:
                    self._state.http.start_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                    data = self._state.http.get_clash_of_code_from_handle(
                        self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        return _start()

    def leave(self):
        """|maybe_coro|

        Leave this Clash Of Code.

        You need to be logged in or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _leave():
                try:
                    await self._state.http.leave_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                    data = await self._state.http.get_clash_of_code_from_handle(
                        self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        else:

            def _leave():
                try:
                    self._state.http.leave_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                    data = self._state.http.get_clash_of_code_from_handle(
                        self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                self._set_data(data)

        return _leave()


class Player(BaseUser):
    """Represents a Clash of Code player.

    Attributes
    -----------
        clash_of_code: :class:`ClashOfCode`
            Clash of Code the Player belongs to.

        public_handle: :class:`str`
            Public handle of the CodinGamer (hexadecimal str).
            Sometimes missing, prefer :attr:`id`.

        id: :class:`int`
            ID of the CodinGamer. Last 7 digits of the :attr:`public_handle`
            reversed.

        pseudo: :class:`int`
            Pseudo of the CodinGamer.

        avatar: Optional :class:`int`
            Avatar ID of the CodinGamer.
            You can get the avatar url with :attr:`avatar_url`.

        cover: Optional :class:`int`
            Cover ID of the CodinGamer. In this case, always ``None``.

        started: :class:`bool`
            Whether the Clash of Code is started.

        finished: :class:`bool`
            Whether the Clash of Code is finished.

        status: :class:`str`
            Status of the Player. Can be ``OWNER`` or ``STANDARD``.

            .. note::
                You can use :attr:`owner` to get a :class:`bool` that describes
                whether the player is the owner.

        owner: :class:`bool`
            Whether the player is the Clash of Code owner.

        position: Optional :class:`int`
            Join position of the Player.

        rank: Optional :class:`int`
            Rank of the Player. Only use this when the Clash of Code is finished
            because it isn't precise until then.

        duration: Optional :class:`~datetime.timedelta`
            Time taken by the player to solve the problem of the Clash of Code.

        language_id: Optional :class:`str`
            Language ID of the language the player used in the Clash of Code.

        score: Optional :class:`int`
            Score of the Player (between 0 and 100).

        code_length: Optional :class:`int`
            Length of the Player's code.
            Only available when the Clash of Code's mode is ``SHORTEST``.

        solution_shared: Optional :class:`bool`
            Whether the Player shared his code.

        submission_id: Optional :class:`int`
            ID of the player's submission.
    """

    clash_of_code: ClashOfCode
    public_handle: str
    id: int
    pseudo: Optional[str]
    avatar: Optional[int]
    cover: Optional[int]
    started: bool
    finished: bool
    status: PlayerStatus
    owner: bool
    position: Optional[int]
    rank: Optional[int]
    duration: Optional[timedelta]
    language_id: Optional[LanguageId]
    score: Optional[int]
    code_length: Optional[int]
    solution_shared: Optional[bool]
    submission_id: Optional[int]

    __slots__ = (
        "clash_of_code",
        "started",
        "finished",
        "status",
        "owner",
        "position",
        "rank",
        "duration",
        "language_id",
        "score",
        "code_length",
        "solution_shared",
        "submission_id",
        "test_session_status",
        "test_session_handle",
    )

    def __init__(
        self,
        state: "ConnectionState",
        coc: ClashOfCode,
        started: bool,
        finished: bool,
        data: dict,
    ):
        self.clash_of_code: ClashOfCode = coc

        self.public_handle = data.get("codingamerHandle")
        self.id = data["codingamerId"]
        self.pseudo = data["codingamerNickname"]
        self.avatar = data.get("codingamerAvatarId")
        self.cover = None

        self.started = started
        self.finished = finished

        self.status = data["status"]
        self.owner = self.status == "OWNER"
        self.position = data.get("position")
        self.rank = data.get("rank")

        self.duration = (
            timedelta(milliseconds=data["duration"])
            if "duration" in data
            else None
        )
        self.language_id = data.get("languageId")
        self.score = data.get("score")
        self.code_length = data.get("criterion")
        self.solution_shared = data.get("solutionShared")
        self.submission_id = data.get("submissionId")

        self.test_session_status = data.get("testSessionStatus")
        self.test_session_handle = data.get("testSessionHandle")

        super().__init__(state)

    def __repr__(self) -> str:
        return (
            "<Player public_handle={0.public_handle!r} pseudo={0.pseudo!r} "
            "position={0.position!r} rank={0.rank!r} duration={0.duration!r} "
            "score={0.score!r} language_id={0.language_id!r}>".format(self)
        )
