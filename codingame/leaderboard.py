import typing

from .abc import BaseUser


class RankedCodinGamer(BaseUser):
    public_handle: str
    id: int
    level: int
    country_id: typing.Optional[str]
    category: typing.Optional[str]
    student: bool
    professional: bool

    rank: int
    score: float

    pseudo: typing.Optional[str]
    company: typing.Optional[str]
    school: typing.Optional[str]
    avatar: typing.Optional[int]
    cover: None
    avatar_url: typing.Optional[str]
    cover_url: None

    leaderboard: "Leaderboard"

    def __init__(self, client, leaderboard: "Leaderboard", data: dict):
        self._client = client
        self.leaderboard = leaderboard

        codingamer = data["codingamer"]
        self.public_handle = codingamer["publicHandle"]
        self.id = codingamer["userId"]
        self.rank = data["rank"]
        self.level = codingamer["level"]
        self.country_id = codingamer.get("countryId")

        self.category = (
            codingamer["category"]
            if codingamer.get("category", "UNKNOWN") != "UNKNOWN"
            else None
        )
        self.student = self.category == "STUDENT"
        self.professional = self.category == "PROFESSIONAL"

        self.rank = data["rank"]
        self.score = data["score"]

        self.pseudo = codingamer.get("pseudo", None) or None
        self.company = data.get("company", None) or None
        self.school = data.get("school", None) or None

        self.avatar = data.get("avatar", None)
        self.cover = None  # not included in leaderboard data

    def __repr__(self):
        return (
            "<{0.__class__.__name__} id={0.id!r} pseudo={0.pseudo!r} "
            "rank={0.rank!r}>".format(self)
        )


class Leaderboard:
    USER_CLASS: typing.Type[RankedCodinGamer] = RankedCodinGamer

    count: int
    users: typing.List[USER_CLASS]

    def __init__(self, client, data: dict):
        self._client = client

        self.count = data["count"]
        self.users = [
            self.USER_CLASS(client, self, user) for user in data["users"]
        ]

    def __repr__(self):
        return "<{0.__class__.__name__} count={0.count!r}>".format(self)


class GlobalRankedCodinGamer(RankedCodinGamer):
    xp: int
    achievements: int
    clash: int
    codegolf: int
    contests: int
    multi_training: int
    optim: int

    leaderboard: "GlobalLeaderboard"

    def __init__(self, client, leaderboard: "GlobalLeaderboard", data: dict):
        super().__init__(client, leaderboard, data)

        self.xp = data["xp"]
        self.achievements = data["achievements"]
        self.clash = data["clash"]
        self.codegolf = data["codegolf"]
        self.contests = data["contests"]
        self.multi_training = data["multiTraining"]
        self.optim = data["optim"]


class GlobalLeaderboard(Leaderboard):
    USER_CLASS = GlobalRankedCodinGamer

    type: str
    group: str
    page: int

    def __init__(self, client, lb_type: str, group: str, page: int, data: dict):
        super().__init__(client, data)
        self.type = lb_type
        self.group = group
        self.page = page

    def __repr__(self):
        return (
            "<{0.__class__.__name__} count={0.count!r} type={0.type!r} "
            "group={0.group!r} page={0.page!r}>".format(self)
        )


class League:
    NAMES = [
        "Legend",
        "Gold",
        "Silver",
        "Bronze",
        "Wood 1",
        "Wood 2",
        "Wood 3",
        "Wood 4",
    ]

    index: int
    count: int
    name: str

    def __init__(self, client, data: dict):
        self._client = client
        league_count: int = data["divisionCount"]
        names = self.NAMES[league_count - 1 :: -1]
        self.index = data["divisionIndex"]
        self.count = data["divisionAgentsCount"]
        self.name = names[self.index]

    def __eq__(self, other: "League"):
        return self.index == other.index

    def __repr__(self):
        return (
            "<{0.__class__.__name__} index={0.index!r} name={0.name!r} "
            "count={0.count!r}>".format(self)
        )


class ChallengeRankedCodinGamer(RankedCodinGamer):
    percentage: typing.Optional[int]
    progress: typing.Optional[str]
    programming_language: str
    test_session_handle: str
    league_rank: typing.Optional[int]
    global_rank: typing.Optional[int]
    league: typing.Optional[League]

    leaderboard: "ChallengeLeaderboard"

    def __init__(self, client, leaderboard: "ChallengeLeaderboard", data: dict):
        super().__init__(client, leaderboard, data)

        self.percentage = data.get("percentage")
        self.progress = data.get("progress")  # idk what this is
        self.programming_language = data["programmingLanguage"]
        self.test_session_handle = data["testSessionHandle"]
        self.league_rank = data.get("localRank")
        self.global_rank = data.get("globalRank")
        self.league = None
        if "league" in data:
            self.league = self.leaderboard.leagues[
                data["league"]["divisionIndex"]
            ]


class ChallengeLeaderboard(Leaderboard):
    USER_CLASS = ChallengeRankedCodinGamer

    name: str
    leagues: typing.List[League]
    group: str
    programming_languages: typing.Dict[str, int]

    def __init__(self, client, name: str, group: str, data: dict):
        self.leagues = [
            League(client, league)
            for league in data.get("leagues", {}).values()
        ]
        super().__init__(client, data)
        self.name = name
        self.group = group
        self.programming_languages = data["programmingLanguages"]

    def __repr__(self):
        return (
            "<{0.__class__.__name__} name={0.name!r} count={0.count!r} "
            "group={0.group!r}>".format(self)
        )


class PuzzleRankedCodinGamer(RankedCodinGamer):
    percentage: typing.Optional[int]
    progress: typing.Optional[str]
    programming_language: str
    test_session_handle: str
    league_rank: typing.Optional[int]
    global_rank: typing.Optional[int]
    league: typing.Optional[League]

    leaderboard: "PuzzleLeaderboard"

    def __init__(self, client, leaderboard: "PuzzleLeaderboard", data: dict):
        super().__init__(client, leaderboard, data)

        self.percentage = data.get("percentage")
        self.progress = data.get("progress")  # idk what this is
        self.programming_language = data["programmingLanguage"]
        self.test_session_handle = data["testSessionHandle"]
        self.league_rank = data.get("localRank")
        self.global_rank = data.get("globalRank")
        self.league = None
        if "league" in data:
            self.league = self.leaderboard.leagues[
                data["league"]["divisionIndex"]
            ]


class PuzzleLeaderboard(Leaderboard):
    USER_CLASS = PuzzleRankedCodinGamer

    name: str
    leagues: typing.List[League]
    group: str
    programming_languages: typing.Dict[str, int]

    def __init__(self, client, name: str, group: str, data: dict):
        self.leagues = [
            League(client, league)
            for league in data.get("leagues", {}).values()
        ]
        super().__init__(client, data)
        self.name = name
        self.group = group
        self.programming_languages = data["programmingLanguages"]

    def __repr__(self):
        return (
            "<{0.__class__.__name__} name={0.name!r} count={0.count!r} "
            "group={0.group!r}>".format(self)
        )
