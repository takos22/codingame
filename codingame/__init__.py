"""
CodinGame API Wrapper
=====================

Wrapper for the undocumented CodinGame API.
"""

from typing import NamedTuple

VersionInfo = NamedTuple(
    "VersionInfo", major=int, minor=int, micro=int, releaselevel=str, serial=int
)

version_info = VersionInfo(major=1, minor=0, micro=1, releaselevel="", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "1.0.1"

from .clash_of_code import ClashOfCode, Player
from .client import Client
from .codingamer import CodinGamer
from .exceptions import (
    ChallengeNotFound,
    ClashOfCodeNotFound,
    CodinGameAPIError,
    CodinGamerNotFound,
    EmailNotLinked,
    EmailRequired,
    IncorrectPassword,
    LoginError,
    LoginRequired,
    MalformedEmail,
    NotFound,
    PasswordRequired,
    PuzzleNotFound,
)
from .leaderboard import (
    ChallengeLeaderboard,
    ChallengeRankedCodinGamer,
    GlobalLeaderboard,
    GlobalRankedCodinGamer,
    League,
    PuzzleLeaderboard,
    PuzzleRankedCodinGamer,
)
from .notification import Notification

__all__ = (
    # Client
    Client,
    # CodinGamer
    CodinGamer,
    # Clash of Code
    ClashOfCode,
    Player,
    # Notification
    Notification,
    # Leaderboard
    GlobalLeaderboard,
    GlobalRankedCodinGamer,
    League,
    ChallengeLeaderboard,
    ChallengeRankedCodinGamer,
    PuzzleLeaderboard,
    PuzzleRankedCodinGamer,
    # Exceptions
    CodinGameAPIError,
    LoginError,
    EmailRequired,
    MalformedEmail,
    PasswordRequired,
    EmailNotLinked,
    IncorrectPassword,
    LoginRequired,
    NotFound,
    CodinGamerNotFound,
    ClashOfCodeNotFound,
    ChallengeNotFound,
    PuzzleNotFound,
)
