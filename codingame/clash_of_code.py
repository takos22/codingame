import requests
from datetime import datetime

from typing import List

from .endpoints import Endpoints


class ClashOfCode:
    """Represents a Clash of Code.

    Do not create this class yourself. Only get it through :meth:`Client.get_clash_of_code()`.

    Attributes
    -----------
    public_handle: :class:`str`
        Public handle of the Clash of Code (hexadecimal str).

    public: :class:`bool`
        If the Clash of Code is public.

    min_players: :class:`int`
        Minimum number of players.

    max_players: :class:`int`
        Maximum number of players.

    modes: :class:`list`
        List of possible modes.

    programming_languages: :class:`list`
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

    end_time: :class:`datetime.datetime`
        Start time of the Clash of Code.

    time_before_start: :class:`float`
        Time before the start of the Clash of Code (in seconds).

    time_before_end: :class:`float`
        Time before the end of the Clash of Code (in seconds).

    players: List[:class:`Player`]
        List of the players in the Clash of Code.
    """

    def __init__(self, *, session: requests.Session, **data):
        self._session: requests.Session = session

        self.public_handle: str = data["publicHandle"]
        self.public: bool = data["publicClash"]
        self.min_players: int = data["nbPlayersMin"]
        self.max_players: int = data["nbPlayersMax"]
        self.modes: list = data["modes"]
        self.programming_languages: list = data["programmingLanguages"]

        self.started: bool = data["started"]
        self.finished: bool = data["finished"]
        self.mode: str or None = data.get("mode", None)

        dt_format = "%b %d, %Y %I:%M:%S %p"
        self.creation_time: datetime = datetime.strptime(data["creationTime"], dt_format)
        self.start_time: datetime = datetime.strptime(data["startTime"], dt_format)
        self.end_time: datetime = datetime.strptime(data["endTime"], dt_format)

        self.time_before_start: float = data["msBeforeStart"] / 1000
        self.time_before_end: float = data["msBeforeEnd"] / 1000

        self.players: List[Player] = [
            Player(
                session=self._session, coc=self, started=self.started,
                finished=self.finished, **player
            )
            for player in data["players"]
        ]

    def __repr__(self):
        return (
            "<ClashOfCode public_handle={0.public_handle!r} public={0.public!r} "
            "modes={0.modes!r} programming_languages={0.programming_languages!r} "
            "started={0.started!r} finished={0.finished!r} players={0.players!r}>".format(self)
        )


class Player:
    """Represents a Clash of Code player.

    Do not create this class yourself. Only get it through :attr:`ClashOfCode.players`.

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

    position: :class:`int`
        Join position of the Player.

    rank: :class:`int`
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

    solution_shared: Optional[:class:`int`]
        ID of the player's submission.
    """

    def __init__(
        self, *, session: requests.Session, coc: ClashOfCode, started: bool,
        finished: bool, **data
    ):
        self._session: requests.Session = session
        self.clash_of_code: ClashOfCode = coc

        self.public_handle: str = data["codingamerHandle"]
        self.id: int = data["codingamerId"]
        self.pseudo: int = data["codingamerNickname"]
        self.avatar: int or None = data.get("codingamerAvatarId", None)
        self.avatar_url: str or None = f"https://static.codingame.com/servlet/fileservlet?id={self.avatar}" if self.avatar else None

        self.started: bool = started
        self.finished: bool = finished

        self.status: str = data["status"]
        self.owner: bool = self.status == "OWNER"
        self.position: int = data["position"]
        self.rank: int = data["rank"]

        self.duration: float or None = data["duration"] / 1000 or None
        self.language_id: str or None = data.get("languageId", None)
        self.score: int or None = data.get("score", None)
        self.code_length: int or None = data.get("criterion", None)
        self.solution_shared: bool or None = data.get("solutionShared", None)
        self.submission_id: int or None = data.get("submissionId", None)

    # TODO: find a way to get the solution code without getting a 561 error
    # @property
    # def solution(self):
    #     if not self.finished or not self.solution_shared:
    #         return

    #     r = self._session.post(Endpoints.Solution, json=[self.id, self.submission_id])
    #     return r.json()["code"]

    def __repr__(self):
        return (
            "<Player public_handle={0.public_handle!r} pseudo={0.pseudo!r} "
            "position={0.position!r} rank={0.rank!r} duration={0.duration!r} "
            "score={0.score!r} language_id={0.language_id!r}>".format(self)
        )
