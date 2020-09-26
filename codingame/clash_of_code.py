from datetime import datetime

from typing import List, Optional

from .abc import BaseUser


class ClashOfCode:
    """Represents a Clash of Code.

    Do not create this class yourself. Only get it through :meth:`Client.get_clash_of_code()`.

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the Clash of Code (hexadecimal str).

        join_url: :class:`str`
            URL to join the Clash of Code.

        public: :class:`bool`
            If the Clash of Code is public.

        min_players: :class:`int`
            Minimum number of players.

        max_players: :class:`int`
            Maximum number of players.

        modes: Optional[:class:`list`]
            List of possible modes.

        programming_languages: Optional[:class:`list`]
            List of possible programming languages.

        started: :class:`bool`
            If the Clash of Code is started.

        finished: :class:`bool`
            If the Clash of Code is finished.

        mode: :class:`str`
            The mode of the Clash of Code.

        creation_time: :class:`datetime.datetime`
            Creation time of the Clash of Code.

        start_time: :class:`datetime.datetime`
            Start time of the Clash of Code.

        end_time: Optional[:class:`datetime.datetime`]
            Start time of the Clash of Code.

        time_before_start: :class:`float`
            Time before the start of the Clash of Code (in seconds).

        time_before_end: Optional[:class:`float`]
            Time before the end of the Clash of Code (in seconds).

        players: List[:class:`Player`]
            List of the players in the Clash of Code.
    """

    def __init__(self, *, client, **data):
        self._client = client

        self.public_handle: str = data["publicHandle"]
        self.join_url: str = f"https://www.codingame.com/clashofcode/clash/{self.public_handle}"
        self.public: bool = data["publicClash"]
        self.min_players: int = data["nbPlayersMin"]
        self.max_players: int = data["nbPlayersMax"]
        self.modes: Optional[List] = data.get("modes", None)
        self.programming_languages: Optional[List] = data.get("programmingLanguages", None)

        self.started: bool = data["started"]
        self.finished: bool = data["finished"]
        self.mode: Optional[str] = data.get("mode", None)

        dt_format = "%b %d, %Y %I:%M:%S %p"
        self.creation_time: datetime = datetime.strptime(data["creationTime"], dt_format)
        self.start_time: datetime = datetime.strptime(data["startTime"], dt_format)
        self.end_time: Optional[datetime] = datetime.strptime(data["endTime"], dt_format) if "endTime" in data else None

        self.time_before_start: float = data["msBeforeStart"] / 1000
        self.time_before_end: Optional[float] = (data["msBeforeEnd"] / 1000) if "msBeforeEnd" in data else None

        self.players: List[Player] = [
            Player(client=self._client, coc=self, started=self.started, finished=self.finished, **player)
            for player in data["players"]
        ]

    def __repr__(self):
        return (
            "<ClashOfCode public_handle={0.public_handle!r} public={0.public!r} "
            "modes={0.modes!r} programming_languages={0.programming_languages!r} "
            "started={0.started!r} finished={0.finished!r} players={0.players!r}>".format(self)
        )


class Player(BaseUser):
    """Represents a Clash of Code player.

    Do not create this class yourself. Only get it through :class:`ClashOfCode.players`.

    Attributes
    -----------
        clash_of_code: :class:`ClashOfCode`
            Clash of Code the Player belongs to.

        public_handle: :class:`str`
            Public handle of the CodinGamer (hexadecimal str).

        id: :class:`int`
            ID of the CodinGamer. Last 7 digits of the :attr:`public_handle` reversed.

        pseudo: :class:`int`
            Pseudo of the CodinGamer.

        avatar: Optional[:class:`int`]
            Avatar ID of the CodinGamer, if set else `None`. You can get the avatar url with :attr:`avatar_url`.

        avatar_url: Optional[:class:`str`]
            Avatar URL of the CodinGamer, if set else `None`.

        started: :class:`bool`
            If the Clash of Code is started.

        finished: :class:`bool`
            If the Clash of Code is finished.

        status: :class:`str`
            Status of the Player. Can be ``OWNER`` or ``STANDARD``.

            .. note::
                You can use :attr:`owner` to get a :class:`bool` that describes the Player's status.

        position: Optional[:class:`int`]
            Join position of the Player.

        rank: Optional[:class:`int`]
            Rank of the Player.

        duration: Optional[:class:`float`]
            Time of the player in the Clash of Code.

        language_id: Optional[:class:`str`]
            Language ID of the language the player used in the Clash of Code.

        score: Optional[:class:`int`]
            Score of the Player (between 0 and 100).

        code_length: Optional[:class:`int`]
            Length of the Player's code. Only available when the Clash of Code's mode is ``SHORTEST``.

        solution_shared: Optional[:class:`bool`]
            If the Player shared his code.

        submission_id: Optional[:class:`int`]
            ID of the player's submission.
    """

    clash_of_code: ClashOfCode
    public_handle: str
    id: int
    pseudo: str
    avatar: Optional[int]
    avatar_url: Optional[str]
    started: bool
    finished: bool
    status: str
    owner: bool
    position: Optional[int]
    rank: Optional[int]
    duration: Optional[float]
    language_id: Optional[str]
    score: Optional[int]
    code_length: Optional[int]
    solution_shared: Optional[bool]
    submission_id: Optional[int]

    def __init__(self, *, client, coc: ClashOfCode, started: bool, finished: bool, **data):
        self._client = client
        self.clash_of_code: ClashOfCode = coc

        self.public_handle = data["codingamerHandle"]
        self.id = data["codingamerId"]
        self.pseudo = data["codingamerNickname"]
        self.avatar = data.get("codingamerAvatarId", None)

        self.started = started
        self.finished = finished

        self.status = data["status"]
        self.owner = self.status == "OWNER"
        self.position = data.get("position", None)
        self.rank = data.get("rank", None)

        self.duration = data["duration"] / 1000 or None
        self.language_id = data.get("languageId", None)
        self.score = data.get("score", None)
        self.code_length = data.get("criterion", None)
        self.solution_shared = data.get("solutionShared", None)
        self.submission_id = data.get("submissionId", None)

    # TODO: find a way to get the solution code without getting a 561 error
    # @property
    # def solution(self):
    #     if not self.finished or not self.solution_shared:
    #         return

    #     r = self.client._session.post(Endpoints.Solution, json=[self.id, self.submission_id])
    #     return r.json()["code"]

    def __repr__(self):
        return (
            "<Player public_handle={0.public_handle!r} pseudo={0.pseudo!r} "
            "position={0.position!r} rank={0.rank!r} duration={0.duration!r} "
            "score={0.score!r} language_id={0.language_id!r}>".format(self)
        )
