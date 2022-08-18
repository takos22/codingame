"""
CodinGame API Wrapper
=====================

Wrapper for the undocumented CodinGame API.
"""

from typing import NamedTuple

VersionInfo = NamedTuple(
    "VersionInfo", major=int, minor=int, micro=int, releaselevel=str, serial=int
)

version_info = VersionInfo(major=1, minor=4, micro=0, releaselevel="", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "1.4.0"

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
    CareerCandidateData,
    ClashInviteData,
    ClashOverData,
    CommentType,
    Contribution,
    ContributionData,
    ContributionModeratedActionType,
    ContributionModeratedData,
    ContributionType,
    CustomData,
    FeatureData,
    FriendRegisteredData,
    GenericData,
    JobAcceptedData,
    JobExpiredData,
    LanguageMapping,
    LeagueData,
    NewBlogData,
    NewCommentData,
    NewHintData,
    NewLevelData,
    NewPuzzleData,
    NewWorkBlogData,
    Notification,
    NotificationData,
    NotificationType,
    NotificationTypeGroup,
    OfferApplyData,
    PuzzleOfTheWeekData,
    PuzzleSolution,
    QuestCompletedData,
    TestFinishedData,
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
    ContributionData,
    FeatureData,
    NewHintData,
    ContributionModeratedData,
    NewPuzzleData,
    PuzzleOfTheWeekData,
    QuestCompletedData,
    FriendRegisteredData,
    NewLevelData,
    GenericData,
    CustomData,
    CareerCandidateData,
    TestFinishedData,
    JobAcceptedData,
    JobExpiredData,
    NewWorkBlogData,
    OfferApplyData,
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
