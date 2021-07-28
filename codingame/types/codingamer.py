"""
codingame.types.codingamer
~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `CodinGamer/` endpoints of the CodinGame API.
"""

from typing import Dict, List, Optional

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

__all__ = (
    "PartialCodinGamer",
    "CodinGamerFromID",
    "CodinGamerFromHandle",
    "PointsStatsFromHandle",
    "Follower",
    "Following",
)


class _FormValues(TypedDict):
    school: Optional[str]
    company: Optional[str]  # not sure if company is in form values
    city: Optional[str]


class _BaseCodinGamer(TypedDict, total=False):
    userId: int
    publicHandle: str
    countryId: str
    enable: bool
    pseudo: Optional[str]
    avatar: Optional[int]
    cover: Optional[int]


class PartialCodinGamer(_BaseCodinGamer, total=True):
    pass


class _BaseCodinGamerInfo(_BaseCodinGamer, total=False):
    level: int
    tagline: Optional[str]


class _BaseCodinGamerFrom(_BaseCodinGamerInfo, total=False):
    formValues: _FormValues
    schoolId: Optional[int]
    company: Optional[str]
    biography: Optional[str]
    city: Optional[str]


class CodinGamerFromID(_BaseCodinGamerFrom, total=True):
    pass


_Category = Literal["STUDENT", "PROFESSIONAL", "UNKNOWN"]


class CodinGamerFromHandle(_BaseCodinGamerFrom, total=True):
    rank: int
    xp: int
    category: _Category
    onlineSince: Optional[int]


class _RankHistorics(TypedDict):
    ranks: List[int]
    totals: List[int]
    points: List[int]
    contestPoints: List[int]
    optimPoints: List[int]
    codegolfPoints: List[int]
    multiTrainingPoints: List[int]
    clashPoints: List[int]
    dates: List[int]


class _PointsRankingDto(TypedDict):
    rankHistorics: _RankHistorics
    codingamePointsTotal: int
    codingamePointsRank: int
    codingamePointsContests: int
    codingamePointsAchievements: int
    codingamePointsXp: int
    codingamePointsOptim: int
    codingamePointsCodegolf: int
    codingamePointsMultiTraining: int
    codingamePointsClash: int
    numberCodingamers: int
    numberCodingamersGlobal: int


class _XpThreshold(TypedDict):
    level: int
    xpThreshold: int
    cumulativeXp: int
    rewardLanguages: Optional[Dict[int, str]]


class PointsStatsFromHandle(TypedDict):
    codingamerPoints: int
    achievementCount: int
    codingamer: CodinGamerFromHandle
    codingamePointsRankingDto: _PointsRankingDto
    xpThresholds: List[_XpThreshold]


class _BaseFriend(_BaseCodinGamerInfo, total=False):
    rank: int
    points: int
    isFollowing: bool
    isFollower: bool
    schoolField: Optional[str]
    companyField: Optional[str]
    languages: Optional[str]  # actually a json encoded list


class Follower(_BaseFriend, total=True):
    pass


class Following(_BaseFriend, total=True):
    pass
