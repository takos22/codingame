"""
codingame.types.clash_of_code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `ClashOfCode/` endpoints of the CodinGame API.
"""

from typing import List, Optional

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

__all__ = ("ClashOfCode", "Player")

_Status = Literal["OWNER", "STANDARD"]
_TestSessionStatus = Literal["READY", "COMPLETED"]


class Player(TypedDict):
    codingamerId: int
    codingamerHandle: str
    status: _Status
    duration: int  # time spent
    codingamerNickname: Optional[str]
    codingamerAvatarId: Optional[int]
    # available after start
    position: Optional[int]  # join position
    rank: Optional[int]  # not precise until submission
    testSessionHandle: Optional[str]
    testSessionStatus: Optional[_TestSessionStatus]
    # available after submission
    score: Optional[int]  # test case percentage
    criterion: Optional[int]  # code length when mode is SHORTEST
    languageId: Optional[str]  # sometimes available before, but can change
    solutionShared: Optional[bool]
    submissionId: Optional[int]


_Mode = Literal["FASTEST", "REVERSE", "SHORTEST"]
_DurationType = Literal["SHORT"]  # there might be other duration types


class ClashOfCode(TypedDict):
    publicHandle: str
    nbPlayersMin: int
    nbPlayersMax: int
    clashDurationTypeId: _DurationType
    creationTime: str
    startTime: str  # estimation until started
    endTime: Optional[str]  # available when started
    msBeforeStart: int  # estimation until started
    msBeforeEnd: Optional[int]  # available when started
    started: bool
    finished: bool
    publicClash: bool
    players: List[Player]
    modes: Optional[List[_Mode]]  # available in private clashes or when started
    mode: Optional[_Mode]  # available when started
    programmingLanguages: Optional[
        List[str]
    ]  # available in private clashes or when started  # noqa: E501
