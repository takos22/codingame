import typing
from datetime import datetime, timedelta

from .abc import BaseObject, BaseUser

if typing.TYPE_CHECKING:
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

        creation_time: :class:`datetime.datetime`
            Creation time of the Clash of Code.

        start_time: :class:`datetime.datetime`
            Start time of the Clash of Code. If the Clash of Code hasn't started
            yet, this is the expected start time of the Clash of Code.

        end_time: Optional :class:`datetime.datetime`
            End time of the Clash of Code.

        time_before_start: :class:`datetime.timedelta`
            Time before the start of the Clash of Code.

        time_before_end: Optional :class:`datetime.timedelta`
            Time before the end of the Clash of Code.

        players: :class:`list` of :class:`Player`
            List of the players in the Clash of Code.
    """

    public_handle: str
    join_url: str
    public: bool
    min_players: int
    max_players: int
    modes: typing.Optional[typing.List[str]]
    programming_languages: typing.Optional[typing.List[str]]
    started: bool
    finished: bool
    mode: typing.Optional[str]
    creation_time: datetime
    start_time: datetime
    end_time: typing.Optional[datetime]
    time_before_start: timedelta
    time_before_end: typing.Optional[timedelta]
    players: typing.List["Player"]

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

    def __init__(self, state: "ConnectionState", data: dict):
        self.public_handle = data["publicHandle"]
        self.join_url = (
            f"https://www.codingame.com/clashofcode/clash/{self.public_handle}"
        )
        self.public = data["publicClash"]
        self.min_players = data["nbPlayersMin"]
        self.max_players = data["nbPlayersMax"]
        self.modes = data.get("modes")
        self.programming_languages = data.get("programmingLanguages")

        self.started = data["started"]
        self.finished = data["finished"]
        self.mode = data.get("mode")

        dt_format = "%b %d, %Y %I:%M:%S %p"
        self.creation_time = datetime.strptime(data["creationTime"], dt_format)
        self.start_time = datetime.strptime(data["startTime"], dt_format)
        self.end_time = (
            datetime.strptime(data["endTime"], dt_format)
            if "endTime" in data
            else None
        )

        self.time_before_start = timedelta(milliseconds=data["msBeforeStart"])
        self.time_before_end = (
            timedelta(milliseconds=data["msBeforeEnd"])
            if "msBeforeEnd" in data
            else None
        )

        self.players = [
            Player(
                state,
                self,
                self.started,
                self.finished,
                player,
            )
            for player in data["players"]
        ]

        super().__init__(state)

    def __repr__(self) -> str:
        return (
            "<ClashOfCode public_handle={0.public_handle!r} "
            "public={0.public!r} modes={0.modes!r} "
            "programming_languages={0.programming_languages!r} "
            "started={0.started!r} finished={0.finished!r} "
            "players={0.players!r}>".format(self)
        )


class Player(BaseUser):
    """Represents a Clash of Code player.

    Attributes
    -----------
        clash_of_code: :class:`ClashOfCode`
            Clash of Code the Player belongs to.

        public_handle: :class:`str`
            Public handle of the CodinGamer (hexadecimal str).

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

        duration: Optional :class:`datetime.timedelta`
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
    pseudo: typing.Optional[str]
    avatar: typing.Optional[int]
    cover: typing.Optional[int]
    started: bool
    finished: bool
    status: str
    owner: bool
    position: typing.Optional[int]
    rank: typing.Optional[int]
    duration: typing.Optional[timedelta]
    language_id: typing.Optional[str]
    score: typing.Optional[int]
    code_length: typing.Optional[int]
    solution_shared: typing.Optional[bool]
    submission_id: typing.Optional[int]

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

        self.public_handle = data["codingamerHandle"]
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

        super().__init__(state)

    def __repr__(self) -> str:
        return (
            "<Player public_handle={0.public_handle!r} pseudo={0.pseudo!r} "
            "position={0.position!r} rank={0.rank!r} duration={0.duration!r} "
            "score={0.score!r} language_id={0.language_id!r}>".format(self)
        )
