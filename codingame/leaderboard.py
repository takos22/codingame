import typing

from .abc import BaseUser


class RankedCodinGamer(BaseUser):
    """Base ranked CodinGamer.

    Implements the common data for the leaderboard users.
    """

    public_handle: str
    """Public handle of the CodinGamer (hexadecimal str)."""
    id: int
    """ID of the CodinGamer. Last 7 digits of the :attr:`public_handle`
    reversed."""
    pseudo: typing.Optional[str]
    """Pseudo of the CodinGamer."""
    avatar: typing.Optional[int]
    """Avatar ID of the CodinGamer. You can get the avatar url with
    :attr:`avatar_url`."""
    cover: None
    """Cover ID of the CodinGamer. In this case, always ``None``."""

    level: int
    """Level of the CodinGamer.."""
    country_id: typing.Optional[str]
    """ID of the CodinGamer's country."""
    category: typing.Optional[str]
    """Category of the CodinGamer. Can be ``STUDENT`` or ``PROFESSIONAL``."""
    student: bool
    """Whether the CodinGamer is a student."""
    professional: bool
    """Whether the CodinGamer is a professional."""
    school: typing.Optional[str]
    """Company of the CodinGamer."""
    company: typing.Optional[str]
    """School of the CodinGamer."""

    rank: int
    """Rank in the leaderboard of the CodinGamer."""
    score: float
    """Score of the CodinGamer."""

    leaderboard: "Leaderboard"
    """The leaderboard in which this CodinGamer is ranked."""

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
    """Base leaderboard.

    Implements the common data for the leaderboards.
    """

    _USER_CLASS: typing.Type[RankedCodinGamer] = RankedCodinGamer

    count: int
    """Number of users in the leaderboard."""
    users: typing.List[_USER_CLASS]
    """Leaderboard ranking."""

    def __init__(self, client, data: dict):
        self._client = client

        self.count = data["count"]
        self.users = [
            self._USER_CLASS(client, self, user) for user in data["users"]
        ]

    def __repr__(self):
        return "<{0.__class__.__name__} count={0.count!r}>".format(self)


class GlobalRankedCodinGamer(RankedCodinGamer):
    """Ranked CodinGamer in global leaderboard."""

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
    """Global leaderboard."""

    _USER_CLASS = GlobalRankedCodinGamer

    type: str
    """Global leaderboard type. One of GENERAL, CONTESTS, BOT_PROGRAMMING,
    OPTIM, CODEGOLF."""
    group: str
    """Group of CodinGamer who are ranked. One of global, country, company,
    school, following."""
    page: int
    """Page of the leaderboard."""
    users: typing.List[GlobalRankedCodinGamer]
    """Global leaderboard ranking."""

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
    """League in a challenge or puzzle leaserboard."""

    _NAMES = [
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
    """Index of the league."""
    count: int
    """Number of users in the league."""
    name: str
    """Name of the league."""

    def __init__(self, client, data: dict):
        self._client = client
        league_count: int = data["divisionCount"]
        names = self._NAMES[league_count - 1 :: -1]
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
    """Ranked CodinGamer in challenge leaderboards."""

    percentage: typing.Optional[int]
    """Test cases completion percentage of the CodinGamer."""
    progress: typing.Optional[str]
    """Progress of the CodinGamer. I don't understand what this is, so if you
    know, please join the support server and tell me."""
    programming_language: str
    """The programming language used by the CodinGamer in this puzzle."""
    test_session_handle: str
    """The handle of the test session that tested the solution of the
    CodinGamer."""
    league_rank: typing.Optional[int]
    """The rank of the CodinGamer in their league."""
    global_rank: typing.Optional[int]
    """The rank of the CodinGamer in the world."""
    league: typing.Optional[League]
    """The league of the CodinGamer in this puzzle."""

    leaderboard: "ChallengeLeaderboard"
    """The leaderboard that this CodinGamer is part of."""

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
    """Challenge leaderboard."""

    _USER_CLASS = ChallengeRankedCodinGamer

    name: str
    """Name of the challenge."""
    leagues: typing.List[League]
    """Leagues of the challenge. Empty list if no leagues."""
    group: str
    """Group of CodinGamer who are ranked. One of global, country, company,
    school, following."""
    programming_languages: typing.Dict[str, int]
    """Number of CodinGamers who used a language in the challenge."""
    users: typing.List[ChallengeRankedCodinGamer]
    """Challenge leaderboard ranking."""

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
    """Ranked CodinGamer in puzzle leaderboards."""

    percentage: typing.Optional[int]
    """Test cases completion percentage of the CodinGamer."""
    progress: typing.Optional[str]
    """Progress of the CodinGamer. I don't understand what this is, so if you
    know, please join the support server and tell me."""
    programming_language: str
    """The programming language used by the CodinGamer in this puzzle."""
    test_session_handle: str
    """The handle of the test session that tested the solution of the
    CodinGamer."""
    league_rank: typing.Optional[int]
    """The rank of the CodinGamer in their league."""
    global_rank: typing.Optional[int]
    """The rank of the CodinGamer in the world."""
    league: typing.Optional[League]
    """The league of the CodinGamer in this puzzle."""

    leaderboard: "PuzzleLeaderboard"
    """The leaderboard that this CodinGamer is part of."""

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
    """Puzzle leaderboard."""

    _USER_CLASS = PuzzleRankedCodinGamer

    name: str
    """Name of the puzzle."""
    leagues: typing.List[League]
    """Leagues of the puzzle. Empty list if no leagues."""
    group: str
    """Group of CodinGamer who are ranked. One of global, country, company,
    school, following."""
    programming_languages: typing.Dict[str, int]
    """Number of CodinGamers who used a language in the puzzle."""
    users: typing.List[PuzzleRankedCodinGamer]
    """Puzzle leaderboard ranking."""

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
