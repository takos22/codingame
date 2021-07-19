"""
codingame.types.codingamer
~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `CodinGamer/` endpoints of the CodinGame API.
"""

from typing import Optional

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

__all__ = ("CodinGamerFromID", "CodinGamerFromHandle", "Follower", "Following")


class _FormValues(TypedDict):
    school: Optional[str]
    copany: Optional[str]  # not sure if company is in form values
    city: Optional[str]


class _BaseCodinGamer(TypedDict, total=False):
    userId: int
    publicHandle: str
    countryId: str
    level: int
    pseudo: Optional[str]
    avatar: Optional[int]
    cover: Optional[int]
    tagline: Optional[str]


class _BaseCodinGamerFrom(_BaseCodinGamer, total=False):
    formValues: _FormValues
    enable: bool
    schoolId: Optional[int]
    company: Optional[str]
    biography: Optional[str]
    city: Optional[str]


class CodinGamerFromID(_BaseCodinGamerFrom):
    pass


_Category = Literal["STUDENT", "PROFESSIONAL", "UNKNOWN"]


class CodinGamerFromHandle(_BaseCodinGamerFrom):
    rank: int
    xp: int
    category: _Category
    onlineSince: Optional[int]


class _BaseFriend(_BaseCodinGamer, total=False):
    rank: int
    points: int
    isFollowing: bool
    isFollower: bool
    schoolField: Optional[str]
    companyField: Optional[str]
    languages: Optional[str]  # actually a json encoded list


class Follower(_BaseFriend):
    pass


class Following(_BaseFriend):
    pass
