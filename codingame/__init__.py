"""
CodinGame API Wrapper
=====================

Wrapper for the undocumented CodinGame API.
"""

from typing import NamedTuple

VersionInfo = NamedTuple(
    "VersionInfo", major=int, minor=int, micro=int, releaselevel=str, serial=int
)

version_info = VersionInfo(
    major=1, minor=1, micro=0, releaselevel="alpha", serial=0
)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "1.1.0a"

from .clash_of_code import ClashOfCode, Player
from .client import Client
from .codingamer import CodinGamer, PartialCodinGamer
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
from .notification import (
    AchievementUnlockedData,
    ClashInviteData,
    ClashOverData,
    FriendRegisteredData,
    LeagueData,
    NewBlogData,
    NewLevelData,
    Notification,
    NotificationData,
    NotificationType,
    NotificationTypeGroup,
    QuestCompletedData,
)

__all__ = (
    # Client
    Client,
    # CodinGamer
    CodinGamer,
    PartialCodinGamer,
    # Clash of Code
    ClashOfCode,
    Player,
    # Notification
    Notification,
    NotificationType,
    NotificationTypeGroup,
    NotificationData,
    AchievementUnlockedData,
    LeagueData,
    NewBlogData,
    ClashInviteData,
    ClashOverData,
    QuestCompletedData,
    FriendRegisteredData,
    NewLevelData,
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
