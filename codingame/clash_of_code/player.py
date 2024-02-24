from datetime import timedelta
from typing import TYPE_CHECKING, Optional

from ..abc import BaseUser
from ..exceptions import LoginRequired
from ..types.clash_of_code import LanguageId, PlayerStatus
from .solution import Solution

if TYPE_CHECKING:
    from ..state import ConnectionState
    from .clash_of_code import ClashOfCode


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
            Whether the Player shared their code.

        solution_id: Optional :class:`int`
            ID of the player's submission.
    """

    clash_of_code: "ClashOfCode"
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
    solution_id: Optional[int]

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
        "solution_id",
        "submission_id",
        "test_session_status",
        "test_session_handle",
    )

    def __init__(
        self,
        state: "ConnectionState",
        clash_of_code: "ClashOfCode",
        started: bool,
        finished: bool,
        data: dict,
    ):
        self.clash_of_code: "ClashOfCode" = clash_of_code

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
        self.solution_id = data.get("submissionId")
        # TODO decprecate Player.submission_id
        self.submission_id = self.solution_id

        self.test_session_status = data.get("testSessionStatus")
        self.test_session_handle = data.get("testSessionHandle")

        super().__init__(state)

    def __repr__(self) -> str:
        return (
            "<Player public_handle={0.public_handle!r} pseudo={0.pseudo!r} "
            "position={0.position!r} rank={0.rank!r} duration={0.duration!r} "
            "score={0.score!r} language_id={0.language_id!r}>".format(self)
        )

    def get_solution(self) -> Solution:
        if not self._state.logged_in:
            raise LoginRequired()

        if not self.solution_shared:
            raise ValueError()  # TODO raise better error

        if self._state.is_async:

            async def _get_solution():
                solution = await self._state.http.get_solution_by_id(
                    self._state.codingamer.id, self.solution_id
                )
                return Solution(self._state, self.clash_of_code, solution)

        else:

            def _get_solution():
                solution = self._state.http.get_solution_by_id(
                    self._state.codingamer.id, self.solution_id
                )
                return Solution(self._state, self.clash_of_code, solution)

        return _get_solution()
