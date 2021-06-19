"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

from typing import NamedTuple

VersionInfo = NamedTuple(
    "VersionInfo", major=int, minor=int, micro=int, releaselevel=str, serial=int
)

version_info = VersionInfo(major=0, minor=4, micro=0, releaselevel="", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "0.4.0"

__all__ = [
    "Client",
    "CodinGamer",
    "ClashOfCode",
    "Player",
    "Notification",
    "GlobalRankedCodinGamer",
    "GlobalLeaderboard",
    "ChallengeRankedCodinGamer",
    "ChallengeLeaderboard",
    "PuzzleRankedCodinGamer",
    "PuzzleLeaderboard",
    "League",
    "CodinGameAPIError",
    "CodinGamerNotFound",
    "ClashOfCodeNotFound",
    "LoginRequired",
]

from .clash_of_code import ClashOfCode, Player
from .client import Client
from .codingamer import CodinGamer
from .exceptions import (
    ClashOfCodeNotFound,
    CodinGameAPIError,
    CodinGamerNotFound,
    LoginRequired,
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
