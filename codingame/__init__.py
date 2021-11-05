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
    major=1, minor=3, micro=0, releaselevel="alpha", serial=0
)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "1.3.0.alpha0"

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
    WrongCaptchaAnswer,
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
    CommentType,
    Contribution,
    ContributionData,
    ContributionModeratedActionType,
    ContributionModeratedData,
    ContributionType,
    FeaturedData,
    FriendRegisteredData,
    LanguageMapping,
    LeagueData,
    NewBlogData,
    NewCommentData,
    NewCommentResponseData,
    NewHintData,
    NewLevelData,
    NewPuzzleData,
    Notification,
    NotificationData,
    NotificationType,
    NotificationTypeGroup,
    PuzzleOfTheWeekData,
    PuzzleSolution,
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
    ContributionType,
    CommentType,
    ContributionModeratedActionType,
    LanguageMapping,
    NotificationData,
    AchievementUnlockedData,
    LeagueData,
    NewBlogData,
    ClashInviteData,
    ClashOverData,
    Contribution,
    PuzzleSolution,
    NewCommentData,
    NewCommentResponseData,
    ContributionData,
    FeaturedData,
    NewHintData,
    ContributionModeratedData,
    NewPuzzleData,
    PuzzleOfTheWeekData,
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
    WrongCaptchaAnswer,
    LoginRequired,
    NotFound,
    CodinGamerNotFound,
    ClashOfCodeNotFound,
    ChallengeNotFound,
    PuzzleNotFound,
)
