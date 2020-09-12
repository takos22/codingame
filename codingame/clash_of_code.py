from typing import List
import requests

from .endpoints import Endpoints

class ClashOfCode:
    """Represents a Clash of Code.

    Do not create this class yourself. Only get it through :meth:`Client.get_clash_of_code()`.
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
    """Represents a Clash of Code player."""

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
        self.owner: bool = data["status"] == "OWNER"
        self.position: int = data["position"]
        self.rank: int = data["rank"]

        self.duration: float or None = data["duration"] / 1000 or None
        self.language_id: str or None = data.get("languageId", None)
        self.score: int or None = data.get("score", None)
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
