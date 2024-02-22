"""
codingame.types.clash_of_code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `ClashOfCode/` endpoints of the CodinGame API.
"""

from typing import List, Literal, Optional, TypedDict

from .codingamer import PartialCodinGamer

__all__ = (
    "ClashOfCode",
    "Mode",
    "Modes",
    "LanguageId",
    "LanguageIds",
    "DurationType",
    "Player",
    "PlayerStatus",
    "PlayerTestSessionStatus",
    "PartialClashOfCodeTestSession",
    "TestCase",
    "Question",
    "ClashOfCodeTestSession",
)

PlayerStatus = Literal["OWNER", "STANDARD"]
PlayerTestSessionStatus = Literal["READY", "COMPLETED"]

Mode = Literal["FASTEST", "REVERSE", "SHORTEST"]
Modes = List[Mode]
LanguageId = str
LanguageIds = List[LanguageId]
DurationType = Literal["SHORT"]  # there might be other duration types


class Player(TypedDict):
    codingamerId: int
    codingamerHandle: str
    status: PlayerStatus
    duration: int  # time spent
    codingamerNickname: Optional[str]
    codingamerAvatarId: Optional[int]
    # available after start
    position: Optional[int]  # join position
    rank: Optional[int]  # not precise until submission
    testSessionHandle: Optional[str]
    testSessionStatus: Optional[PlayerTestSessionStatus]
    # available after submission
    score: Optional[int]  # test case percentage
    criterion: Optional[int]  # code length when mode is SHORTEST
    languageId: Optional[
        LanguageId
    ]  # sometimes available before, but can change
    solutionShared: Optional[bool]
    submissionId: Optional[int]


class ClashOfCode(TypedDict):
    publicHandle: str
    nbPlayersMin: int
    nbPlayersMax: int
    clashDurationTypeId: DurationType
    # creationTime: str
    # startTime: str  # estimation until started
    # endTime: Optional[str]  # available when started
    startTimestamp: int
    msBeforeStart: int  # estimation until started
    msBeforeEnd: Optional[int]  # available when started
    started: bool
    finished: bool
    # publicClash: bool
    type: str
    players: List[Player]
    modes: Optional[Modes]  # available in private clashes or when started
    mode: Optional[Mode]  # available when started
    programmingLanguages: Optional[
        LanguageIds
    ]  # available in private clashes or when started


class PartialClashOfCodeTestSession(TypedDict):
    direct: bool
    handle: str
    reportReady: bool


class _PartialQuestion(TypedDict):
    questionId: int
    title: str
    hasResult: bool


class TestCase(TypedDict):
    index: int
    inputBinaryId: int
    outputBinaryId: int


class _Language(TypedDict):
    id: str
    name: str


class Contribution(TypedDict):
    moderators: List[PartialCodinGamer]
    type: str
    status: str


class Question(TypedDict):
    testCases: List[TestCase]
    availableLanguages: List[_Language]
    stubGenerator: str
    id: int
    initialId: int
    type: str
    statement: str  # html format
    duration: int
    userId: int
    contribution: Contribution
    contributor: PartialCodinGamer
    index: int
    mode: str
    title: str


class _CurrentQuestion(TypedDict):
    question: Question
    answer: dict


class ClashOfCodeTestSession(TypedDict):
    clash: ClashOfCode
    testType: str
    currentQuestion: _CurrentQuestion
    direct: bool
    questions: List[_PartialQuestion]
    testSessionId: int
    testSessionHandle: str
    needAccount: bool
    shareable: bool
    userId: int
    showReplayPrompt: bool
