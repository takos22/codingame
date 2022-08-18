"""
codingame.types.notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typings for the `Notifications/` endpoints of the CodinGame API.
"""

from typing import Dict, Optional, Union

try:
    from typing import Literal, TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import Literal, TypedDict

    Literal.__module__ = TypedDict.__module__ = "typing"

from .codingamer import PartialCodinGamer

__all__ = (
    "NotificationTypeGroup",
    "NotificationType",
    "NotificationData",
    "Notification",
    "FollowingData",
    "FriendRegisteredData",
    "InvitationAcceptedData",
    "ContestScheduledData",
    "ContestSoonData",
    "ContestStartedData",
    "ContestOverData",
    "NewCommentData",
    "NewCommentResponseData",
    "ClashInviteData",
    "ClashOverData",
    "AchievementUnlockedData",
    "NewLevelData",
    "NewBlogData",
    "FeatureData",
    "NewLeagueData",
    "ElligibleForNextLeagueData",
    "PromotedLeague",
    "ContributionReceivedData",
    "ContributionAcceptedData",
    "ContributionRefusedData",
    "ContributionClashModeRemovedData",
    "NewPuzzleData",
    "PuzzleOfTheWeekData",
    "NewLeagueOpenedData",
    "NewHintData",
    "ContributionModeratedData",
    "QuestCompletedData",
    "InfoGenericData",
    "WarningGenericData",
    "ImportantGenericData",
    "CustomData",
    "CareerNewCandidateData",
    "CareerUpdateCandidateData",
    "TestFinishedData",
    "JobAcceptedData",
    "JobExpiredData",
    "NewWorkBlogData",
    "OfferApplyData",
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
    # generic
    "info-generic",
    "warning-generic",
    "important-generic",
    # custom
    "custom",
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


class ContestData(TypedDict, total=False):
    contest: str  # name
    publicId: str
    imageId: int


class ContestScheduledData(ContestData, total=True):
    date: int  # UTC timestamp with ms


class ContestSoonData(ContestData, total=True):
    hours: int  # hours until start


class ContestStartedData(ContestData, total=True):
    pass


class ContestOverData(ContestData, total=True):
    rank: int
    playerCount: int


# comment


class ContributionData(TypedDict):
    handle: str
    title: str  # maybe optional
    type: Literal[
        "CLASHOFCODE",
        "PUZZLE_INOUT",
        "PUZZLE_MULTI",
        "PUZZLE_SOLO",
        "PUZZLE_OPTI",
    ]  # maybe optional


class PuzzleSolutionData(TypedDict):
    puzzleId: str
    puzzleDetailsPageUrl: Optional[str]
    testSessionSubmissionId: int


class BaseNewCommentData(TypedDict, total=False):
    type: LanguageMapping


class CompleteNewCommentData(BaseNewCommentData, total=True):
    commentType: Literal["CONTRIBUTION", "SOLUTION"]
    typeData: Union[ContributionData, PuzzleSolutionData]
    commentId: int


class URLNewCommentData(BaseNewCommentData, total=True):
    url: str


NewCommentData = NewCommentResponseData = Union[
    CompleteNewCommentData, URLNewCommentData
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
    id: str
    imageId: int
    points: int
    level: str
    completionTime: int
    label: LanguageMapping


# xp


class NewLevelData(TypedDict):
    level: int
    reward: Optional[LanguageMapping]
    triggerCareerPopup: Optional[bool]


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

# for new-league, new-league-opened, elligible-for-next-league, promoted-league
class LeagueData(TypedDict):
    titleLabel: LanguageMapping
    divisionIndex: int
    divisionCount: int
    divisionOffset: int
    thresholdIndex: int
    thumbnailBinaryId: int
    testSessionHandle: str


NewLeagueData = ElligibleForNextLeagueData = PromotedLeague = LeagueData


# contribution


ContributionReceivedData = ContributionAcceptedData = ContributionData
ContributionRefusedData = ContributionClashModeRemovedData = ContributionData


# puzzle


class NewPuzzleData(TypedDict):
    level: LanguageMapping
    name: LanguageMapping
    image: str  # image url
    puzzleId: int


class PuzzleOfTheWeekData(TypedDict):
    puzzleId: int
    puzzleLevel: str
    puzzlePrettyId: str
    puzzleName: LanguageMapping
    puzzleOfTheWeekImageId: int
    contributorNickname: str
    contributorAvatarId: Optional[int]


NewLeagueOpenedData = LeagueData

# hint


class NewHintData(TypedDict):
    puzzleTitle: LanguageMapping
    thumbnailBinaryId: int
    testSessionHandle: str


# moderation


class ContributionModeratedData(TypedDict):
    actionType: Literal["validate", "deny"]
    contribution: ContributionData


# quest


class QuestCompletedData(TypedDict):
    questId: int
    label: LanguageMapping


# generic


class GenericData(TypedDict):
    description: LanguageMapping
    url: str


InfoGenericData = WarningGenericData = ImportantGenericData = GenericData


# custom


class CustomData(TypedDict):
    title: LanguageMapping
    description: LanguageMapping
    image: str  # url of the image
    url: str


# other


class CareerCandidateData(TypedDict):
    handle: str
    username: Optional[str]
    country: str
    region: str
    avatar: Optional[int]


CareerNewCandidateData = CareerUpdateCandidateData = CareerCandidateData


# no category


class TestFinishedData(TypedDict):
    campaignId: int  # probably
    candidateId: int  # probably
    candidateName: Optional[str]
    candidateEmail: str


class JobAcceptedData(TypedDict):
    jobName: Optional[str]
    jobOfferLocation: str
    challengeId: Optional[int]


class JobExpiredData(TypedDict):
    jobName: Optional[str]


NewWorkBlogData = NewBlogData


class OfferApplyData(TypedDict):
    candidateName: str
    jobName: Optional[str]
    jobOfferLocation: str
    challengeId: Optional[int]
    jobOfferId: Optional[int]
    jobOfferApplicantId: Optional[int]


# notification

NotificationData = Union[
    FollowingData,
    FriendRegisteredData,
    InvitationAcceptedData,
    ContestScheduledData,
    ContestSoonData,
    ContestStartedData,
    ContestOverData,
    NewCommentData,
    NewCommentResponseData,
    ClashInviteData,
    ClashOverData,
    AchievementUnlockedData,
    NewLevelData,
    NewBlogData,
    FeatureData,
    NewLeagueData,
    ElligibleForNextLeagueData,
    PromotedLeague,
    ContributionReceivedData,
    ContributionAcceptedData,
    ContributionRefusedData,
    ContributionClashModeRemovedData,
    NewPuzzleData,
    PuzzleOfTheWeekData,
    NewLeagueOpenedData,
    NewHintData,
    ContributionModeratedData,
    QuestCompletedData,
    InfoGenericData,
    WarningGenericData,
    ImportantGenericData,
    CustomData,
    CareerNewCandidateData,
    CareerUpdateCandidateData,
    TestFinishedData,
    JobAcceptedData,
    JobExpiredData,
    NewWorkBlogData,
    OfferApplyData,
]


class Notification(TypedDict):
    id: int
    type: NotificationType
    typeGroup: NotificationTypeGroup
    priority: int
    urgent: bool
    date: int  # UTC timestamp with ms
    seenDate: Optional[int]  # UTC timestamp with ms
    readDate: Optional[int]  # UTC timestamp with ms
    data: Optional[NotificationData]
    codingamer: Optional[PartialCodinGamer]
