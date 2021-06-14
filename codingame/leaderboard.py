import typing

from .abc import BaseUser


class RankedCodinGamer(BaseUser):
    public_handle: str
    id: int
    level: int
    country_id: str
    category: typing.Optional[str]
    student: bool
    professional: bool

    xp: int
    rank: int
    score: float
    achievements: int
    clash: int
    codegolf: int
    contests: int
    multi_training: int
    optim: int

    pseudo: typing.Optional[str]
    company: typing.Optional[str]
    school: typing.Optional[str]
    avatar: typing.Optional[int]
    cover: None
    avatar_url: typing.Optional[str]
    cover_url: None

    def __init__(self, client, data: dict):
        self._client = client

        codingamer = data["codingamer"]
        self.public_handle = codingamer["public_handle"]
        self.id = codingamer["userId"]
        self.rank = data["rank"]
        self.level = codingamer["level"]
        self.country_id = codingamer["countryId"]

        self.category = (
            codingamer["category"]
            if codingamer.get("category", "UNKNOWN") != "UNKNOWN"
            else None
        )
        self.student = self.category == "STUDENT"
        self.professional = self.category == "PROFESSIONAL"

        self.xp = data["xp"]
        self.rank = data["rank"]
        self.score = data["score"]
        self.achievements = data["achievements"]
        self.clash = data["clash"]
        self.codegolf = data["codegolf"]
        self.contests = data["contests"]
        self.multi_training = data["multiTraining"]
        self.optim = data["optim"]

        self.pseudo = codingamer.get("pseudo", None) or None
        self.company = data.get("company", None) or None
        self.school = data.get("school", None) or None

        self.avatar = data.get("avatar", None)
        self.cover = None  # not included in leaderboard data

class Leaderboard:
    def __init__(self, client, lb_type: str, page: int, data: dict):
        self._client = client

        self.type = lb_type
        self.page = page
        self.count = data["count"]
        self.users = [RankedCodinGamer(client, user) for user in data["users"]]
