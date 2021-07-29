"""
codingame.types.notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `Notifications/` endpoints of the CodinGame API.
"""

from typing import Dict, Optional, Union

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

from .codingamer import PartialCodinGamer

__all__ = (
    "NotificationTypeGroup",
    "NotificationType",
    "NotificationData",
    "Notification",
)

NotificationTypeGroup = Literal[
    "social",
    "contest",
    "comment",
    "clash",
    "other",
    "achievement",
    "xp",
    "blog",
    "feature",
    "arena",
    "contribution",
    "puzzle",
    "hints",
    "moderation",
    "quest",
]
NotificationType = Literal[
    # social
    "following",
    "friend-registered",
    "invitation-accepted",
    # contest
    "contest-scheduled",
    "contest-soon",
    "contest-started",
    "contest-over",
    # comment
    "new-comment",
    "new-comment-response",
    # clash
    "clash-invite",
    "clash-over",
    # achievement
    "achievement-unlocked",
    # xp
    "new-level",
    # blog
    "new-blog",
    # feature
    "feature",
    # arena
    "new-league",
    "eligible-for-next-league",
    "promoted-league",
    # contribution
    "contribution-received",
    "contribution-accepted",
    "contribution-refused",
    "contribution-clash-mode-removed",
    # puzzle
    "new-puzzle",
    "puzzle-of-the-week",
    "new-league-opened",
    # hints
    "new-hint",
    # moderation
    "contribution-moderated",
    # quest
    "quest-completed",
    # custom
    "custom",
    # generic
    "warning-generic",
    "important-generic",
    "info-generic",
    # other
    "career-new-candidate",
    "career-update-candidate",
    # didn't find the category for these
    "test-finished",
    "job-accepted",
    "job-expired",
    "new-work-blog",
    "offer-apply",
    "recruiter-contact",
]

LanguageMapping = Dict[str, str]  # "language": "text"

# social

FollowingData = None


class FriendRegisteredData(TypedDict):
    name: str


InvitationAcceptedData = None

# contest


class _ContestData(TypedDict, total=False):
    contest: str  # name
    publicId: str
    imageId: int


class ContestScheduledData(_ContestData, total=True):
    date: int  # UTC timestamp with ms


class ContestSoonData(_ContestData, total=True):
    hours: int  # hours until start


class ContestStartedData(_ContestData, total=True):
    pass


class ContestOverData(_ContestData, total=True):
    rank: int
    playerCount: int


# comment


class _Contribution(TypedDict):
    handle: str


class _PuzzleSolution(TypedDict):
    puzzleId: str
    puzzleDetailsPageUrl: Optional[str]
    testSessionSubmissionId: int


class _NewCommentData(TypedDict, total=False):
    type: LanguageMapping


class _CompleteNewCommentData(_NewCommentData, total=True):
    commentType: Literal["CONTRIBUTION", "SOLUTION"]
    typeData: Union[_Contribution, _PuzzleSolution]
    commentId: int


class _URLNewCommentData(_NewCommentData, total=True):
    url: str


NewCommentData = NewCommentResponseData = Union[
    _CompleteNewCommentData, _URLNewCommentData
]

# clash


class ClashInviteData(TypedDict):
    handle: str


class ClashOverData(TypedDict):
    handle: str
    rank: int
    playerCount: int


# achievement


class AchievementUnlockedData(TypedDict):
    label: LanguageMapping
    points: int
    level: int
    id: str
    imageId: int


# xp


class NewLevelData(TypedDict):
    level: int


# blog


class NewBlogData(TypedDict):
    title: LanguageMapping
    url: LanguageMapping


# feature


class FeatureData(TypedDict):
    title: Optional[LanguageMapping]
    description: LanguageMapping
    "image-instant"  # : str
    url: str


FeatureData.__annotations__["image-instant"] = str


# arena


class NewLeagueData(TypedDict):
    titleLabel: LanguageMapping
    divisionIndex: int
    thresholdIndex: int


# generic


class GenericData(TypedDict):
    description: LanguageMapping
    url: str


# custom


class CustomData(TypedDict):
    title: LanguageMapping
    descrition: LanguageMapping
    image: str  # url of the image
    url: str


# TODO remove this and separate for every type
class _NotificationData(TypedDict):
    puzzleOfTheWeekImageId: Optional[int]
    contributorNickname: Optional[str]
    contributorAvatarId: Optional[int]
    puzzleId: Optional[int]
    puzzleLevel: Optional[str]
    puzzlePrettyId: Optional[str]
    puzzleName: Optional[dict]


NotificationData = Union[GenericData, CustomData, _NotificationData]


class Notification(TypedDict):
    id: int
    type: NotificationType
    typeGroup: NotificationTypeGroup
    priority: int
    date: int  # UTC timestamp with ms
    urgent: bool
    data: Optional[NotificationData]
    codingamer: Optional[PartialCodinGamer]
