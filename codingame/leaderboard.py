import typing

from .abc import BaseObject, BaseUser

if typing.TYPE_CHECKING:
    from .state import ConnectionState

__all__ = (
    "GlobalRankedCodinGamer",
    "GlobalLeaderboard",
    "League",
    "ChallengeRankedCodinGamer",
    "ChallengeLeaderboard",
    "PuzzleRankedCodinGamer",
    "PuzzleLeaderboard",
)


class BaseRankedCodinGamer(BaseUser):
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

    leaderboard: "BaseLeaderboard"
    """The leaderboard in which this CodinGamer is ranked."""

    __slots__ = (
        "level",
        "country_id",
        "category",
        "student",
        "professional",
        "school",
        "company",
        "rank",
        "score",
        "leaderboard",
    )

    def __init__(
        self,
        state: "ConnectionState",
        leaderboard: "BaseLeaderboard",
        data: dict,
    ):
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

        self.pseudo = codingamer.get("pseudo") or None
        self.company = data.get("company") or None
        self.school = data.get("school") or None

        self.avatar = data.get("avatar")
        self.cover = None  # not included in leaderboard data

        super().__init__(state)

    def __repr__(self):
        return (
            "<{0.__class__.__name__} id={0.id!r} pseudo={0.pseudo!r} "
            "rank={0.rank!r}>".format(self)
        )


class BaseLeaderboard(BaseObject):
    """Base leaderboard.

    Implements the common data for the leaderboards.
    """

    _USER_CLASS: typing.Type[BaseRankedCodinGamer] = BaseRankedCodinGamer

    count: int
    """Number of users in the leaderboard."""
    users: typing.List[_USER_CLASS]
    """Leaderboard ranking."""

    __slots__ = (
        "count",
        "users",
    )

    def __init__(self, state: "ConnectionState", data: dict):
        self.count = data["count"]
        self.users = [
            self._USER_CLASS(state, self, user) for user in data["users"]
        ]

        super().__init__(state)

    def __repr__(self):
        return "<{0.__class__.__name__} count={0.count!r}>".format(self)


class GlobalRankedCodinGamer(BaseRankedCodinGamer):
    """Ranked CodinGamer in global leaderboard."""

    xp: int
    achievements: int
    clash: int
    codegolf: int
    contests: int
    multi_training: int
    optim: int

    leaderboard: "GlobalLeaderboard"

    __slots__ = (
        "xp",
        "achievements",
        "clash",
        "codegolf",
        "contests",
        "multi_training",
        "optim",
    )

    def __init__(
        self,
        state: "ConnectionState",
        leaderboard: "GlobalLeaderboard",
        data: dict,
    ):
        self.xp = data["xp"]
        self.achievements = data["achievements"]
        self.clash = data["clash"]
        self.codegolf = data["codegolf"]
        self.contests = data["contests"]
        self.multi_training = data["multiTraining"]
        self.optim = data["optim"]

        super().__init__(state, leaderboard, data)


class GlobalLeaderboard(BaseLeaderboard):
    """Global leaderboard."""

    _USER_CLASS = GlobalRankedCodinGamer

    type: str
    """Global leaderboard type. One of ``"GENERAL"``, ``"CONTESTS"``,
    ``"BOT_PROGRAMMING"``, ``"OPTIM"``, ``"CODEGOLF"``."""
    group: str
    """Group of CodinGamer who are ranked. One of ``"global"``, ``"country"``,
    ``"company"``, ``"school"``, ``"following"``."""
    page: int
    """Page of the leaderboard."""
    users: typing.List[GlobalRankedCodinGamer]
    """Global leaderboard ranking."""

    __slots__ = (
        "type",
        "group",
        "page",
    )

    def __init__(
        self,
        state: "ConnectionState",
        lb_type: str,
        group: str,
        page: int,
        data: dict,
    ):
        self.type = lb_type
        self.group = group
        self.page = page

        super().__init__(state, data)

    def __repr__(self):
        return (
            "<{0.__class__.__name__} count={0.count!r} type={0.type!r} "
            "group={0.group!r} page={0.page!r}>".format(self)
        )


class League(BaseObject):
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
    users: list
    """Name of the league."""

    __slots__ = (
        "index",
        "count",
        "name",
        "users",
    )

    def __init__(self, state: "ConnectionState", data: dict):
        league_count: int = data["divisionCount"]
        names = self._NAMES[league_count - 1 :: -1]  # noqa: E203
        self.index = data["divisionIndex"]
        self.count = data["divisionAgentsCount"]
        self.name = names[self.index]
        self.users = []

        super().__init__(state)

    def __eq__(self, other: "League"):
        return self.index == other.index

    def __repr__(self):
        return (
            "<{0.__class__.__name__} index={0.index!r} name={0.name!r} "
            "count={0.count!r}>".format(self)
        )


class ChallengeRankedCodinGamer(BaseRankedCodinGamer):
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

    __slots__ = (
        "percentage",
        "progress",
        "programming_language",
        "test_session_handle",
        "league_rank",
        "global_rank",
        "league",
    )

    def __init__(
        self,
        state: "ConnectionState",
        leaderboard: "ChallengeLeaderboard",
        data: dict,
    ):
        self.percentage = data.get("percentage")
        self.progress = data.get("progress")  # idk what this is
        self.programming_language = data["programmingLanguage"]
        self.test_session_handle = data["testSessionHandle"]
        self.league_rank = data.get("localRank")
        self.global_rank = data.get("globalRank")
        self.league = None
        if "league" in data:
            self.league = leaderboard.leagues[data["league"]["divisionIndex"]]
            self.league.users.append(self)

        super().__init__(state, leaderboard, data)


class ChallengeLeaderboard(BaseLeaderboard):
    """Challenge leaderboard."""

    _USER_CLASS = ChallengeRankedCodinGamer

    name: str
    """Name of the challenge."""
    has_leagues: bool
    """Whether the challenge has leagues."""
    leagues: typing.List[League]
    """Leagues of the challenge. Empty list if no leagues."""
    group: str
    """Group of CodinGamer who are ranked. One of ``"global"``, ``"country"``,
    ``"company"``, ``"school"``, ``"following"``."""
    programming_languages: typing.Dict[str, int]
    """Number of CodinGamers who used a language in the challenge."""
    users: typing.List[ChallengeRankedCodinGamer]
    """Challenge leaderboard ranking."""

    __slots__ = (
        "name",
        "has_leagues",
        "leagues",
        "group",
        "programming_languages",
    )

    def __init__(
        self, state: "ConnectionState", name: str, group: str, data: dict
    ):
        self.leagues = [
            League(state, league) for league in data.get("leagues", {}).values()
        ]
        self.has_leagues = bool(self.leagues)
        self.name = name
        self.group = group
        self.programming_languages = data["programmingLanguages"]

        super().__init__(state, data)

    def __repr__(self):
        return (
            "<{0.__class__.__name__} name={0.name!r} count={0.count!r} "
            "group={0.group!r}>".format(self)
        )


class PuzzleRankedCodinGamer(BaseRankedCodinGamer):
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

    __slots__ = (
        "percentage",
        "progress",
        "programming_language",
        "test_session_handle",
        "league_rank",
        "global_rank",
        "league",
    )

    def __init__(
        self,
        state: "ConnectionState",
        leaderboard: "PuzzleLeaderboard",
        data: dict,
    ):
        self.percentage = data.get("percentage")
        self.progress = data.get("progress")  # idk what this is
        self.programming_language = data["programmingLanguage"]
        self.test_session_handle = data["testSessionHandle"]
        self.league_rank = data.get("localRank")
        self.global_rank = data.get("globalRank")
        self.league = None
        if "league" in data:
            self.league = leaderboard.leagues[data["league"]["divisionIndex"]]
            self.league.users.append(self)

        super().__init__(state, leaderboard, data)


class PuzzleLeaderboard(BaseLeaderboard):
    """Puzzle leaderboard."""

    _USER_CLASS = PuzzleRankedCodinGamer

    name: str
    """Name of the puzzle."""
    has_leagues: bool
    """Whether the puzzle has leagues."""
    leagues: typing.List[League]
    """Leagues of the puzzle. Empty list if no leagues."""
    group: str
    """Group of CodinGamer who are ranked. One of ``"global"``, ``"country"``,
    ``"company"``, ``"school"``, ``"following"``."""
    programming_languages: typing.Dict[str, int]
    """Number of CodinGamers who used a language in the puzzle."""
    users: typing.List[PuzzleRankedCodinGamer]
    """Puzzle leaderboard ranking."""

    __slots__ = (
        "name",
        "has_leagues",
        "leagues",
        "group",
        "programming_languages",
    )

    def __init__(
        self, state: "ConnectionState", name: str, group: str, data: dict
    ):
        self.leagues = [
            League(state, league) for league in data.get("leagues", {}).values()
        ]
        self.has_leagues = bool(self.leagues)
        self.name = name
        self.group = group
        self.programming_languages = data["programmingLanguages"]

        super().__init__(state, data)

    def __repr__(self):
        return (
            "<{0.__class__.__name__} name={0.name!r} count={0.count!r} "
            "group={0.group!r}>".format(self)
        )
