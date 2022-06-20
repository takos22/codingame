import re
import typing
from datetime import datetime

from ..abc import Mapping
from ..types import notification as types
from ..utils import to_datetime
from .enums import (
    CommentType,
    ContributionModeratedActionType,
    ContributionType,
    NotificationType,
)

if typing.TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = (
    "LanguageMapping",
    "NotificationData",
    "AchievementUnlockedData",
    "LeagueData",
    "NewBlogData",
    "ClashInviteData",
    "ClashOverData",
    "Contribution",
    "PuzzleSolution",
    "NewCommentData",
    "ContributionData",
    "FeatureData",
    "NewHintData",
    "ContributionModeratedData",
    "NewPuzzleData",
    "PuzzleOfTheWeekData",
    "QuestCompletedData",
    "FriendRegisteredData",
    "NewLevelData",
    "GenericData",
    "CustomData",
    "CareerCandidateData",
    "TestFinishedData",
    "JobAcceptedData",
    "JobExpiredData",
    "NewWorkBlogData",
    "OfferApplyData",
)


class LanguageMapping(Mapping):
    """Mapping to store text with multiple languages.

    This class has the same interface as :class:`dict` for backwards
    compatibility.

    Attributes
    -----------
        en: :class:`str`
            The text in english.

        fr: :class:`str`
            The text in french.
    """

    en: str
    fr: str

    __slots__ = ("en", "fr")

    def __init__(
        self, state: "ConnectionState", mapping: types.LanguageMapping
    ):
        self.en = mapping["en"]
        self.fr = mapping["fr"]

        super().__init__(state, mapping)

    # TODO implement state.current_language
    # def __str__(self) -> str:
    #     return self[state.current_language]


class NotificationData(Mapping):
    """Base class for the notification data classes.

    This class has the same interface as :class:`dict` for backwards
    compatibility.

    Attributes
    -----------
        _raw: :class:`dict`
            Raw data of the :class:`Notification`, useful when one of the values
            isn't an attribute.
    """

    _raw: dict

    def __init__(self, state: "ConnectionState", data: types.NotificationData):
        super().__init__(state, data)

    @classmethod
    def from_type(
        cls,
        type: NotificationType,
        state: "ConnectionState",
        data: types.NotificationData,
    ) -> typing.Optional["NotificationData"]:
        """Create the correct :class:`NotificationData` subclass according to
        the :class:`notification type <NotificationType>`.

        Parameters
        ----------
            type : :class:`NotificationType`
                The notification type.

            data : :class:`dict`
                The notification data.

        Returns
        -------
            :class:`NotificationData`
                The parsed data of the notifcation.
        """

        NT = NotificationType
        type_to_obj = {
            NT.achievement_unlocked: AchievementUnlockedData,
            NT.new_league: LeagueData,
            NT.eligible_for_next_league: LeagueData,
            NT.promoted_league: LeagueData,
            NT.new_league_opened: LeagueData,
            NT.new_blog: NewBlogData,
            NT.clash_invite: ClashInviteData,
            NT.clash_over: ClashOverData,
            NT.new_comment: NewCommentData,
            NT.new_comment_response: NewCommentData,
            NT.contribution_received: ContributionData,
            NT.contribution_accepted: ContributionData,
            NT.contribution_refused: ContributionData,
            NT.contribution_clash_mode_removed: ContributionData,
            NT.feature: FeatureData,
            NT.new_hint: NewHintData,
            NT.contribution_moderated: ContributionModeratedData,
            NT.new_puzzle: NewPuzzleData,
            NT.puzzle_of_the_week: PuzzleOfTheWeekData,
            NT.quest_completed: QuestCompletedData,
            NT.friend_registered: FriendRegisteredData,
            NT.new_level: NewLevelData,
            NT.info_generic: GenericData,
            NT.warning_generic: GenericData,
            NT.important_generic: GenericData,
            NT.custom: CustomData,
            NT.career_new_candidate: CareerCandidateData,
            NT.career_update_candidate: CareerCandidateData,
            NT.test_finished: TestFinishedData,
            NT.job_accepted: JobAcceptedData,
            NT.job_expired: JobExpiredData,
            NT.new_work_blog: NewWorkBlogData,
            NT.offer_apply: OfferApplyData,
        }
        return (
            type_to_obj.get(type, NotificationData)(state, data)
            if data
            else None
        )


# achievement


class AchievementUnlockedData(NotificationData):
    """Data of a :attr:`NotificationType.achievement_unlocked` notification."""

    id: str
    label: LanguageMapping
    points: int
    level: str
    completion_time: datetime
    image_url: str

    __slots__ = (
        "id",
        "label",
        "points",
        "level",
        "completion_time",
        "image_url",
    )

    def __init__(
        self, state: "ConnectionState", data: types.AchievementUnlockedData
    ):
        self.id = data["id"]
        self.label = LanguageMapping(state, data["label"])
        self.points = data["points"]
        self.level = data["level"]
        self.completion_time = to_datetime(data["completionTime"])
        self.image_url = state.http.get_file_url(
            data["imageId"], format="notification_picture"
        )

        super().__init__(state, data)


# arena and new-league-opened


class LeagueData(NotificationData):
    """Data of :attr:`NotificationType.new_league`,
    :attr:`NotificationType.eligible_for_next_league`,
    :attr:`NotificationType.promoted_league` and
    :attr:`NotificationType.new_league_opened` notifications."""

    title_label: LanguageMapping
    division_index: int
    division_count: int
    division_offset: int
    threshold_index: int
    thumbnail_url: str
    test_session_handle: str

    __slots__ = (
        "title_label",
        "division_index",
        "division_count",
        "division_offset",
        "threshold_index",
        "thumbnail_url",
        "test_session_handle",
    )

    def __init__(self, state: "ConnectionState", data: types.LeagueData):
        self.title_label = LanguageMapping(state, data["titleLabel"])
        self.division_index = data["divisionIndex"]
        self.division_count = data["divisionCount"]
        self.division_offset = data["divisionOffset"]
        self.threshold_index = data["thresholdIndex"]
        self.thumbnail_url = state.http.get_file_url(
            data["thumbnailBinaryId"], format="notification_picture"
        )
        self.test_session_handle = data["testSessionHandle"]

        super().__init__(state, data)


# blog


class NewBlogData(NotificationData):
    """Data of a :attr:`NotificationType.new_blog` notification."""

    title: LanguageMapping
    url: LanguageMapping

    __slots__ = (
        "title",
        "url",
    )

    def __init__(self, state: "ConnectionState", data: types.NewBlogData):
        self.title = LanguageMapping(state, data["title"])
        self.url = LanguageMapping(state, data["url"])

        super().__init__(state, data)


# clash


class ClashInviteData(NotificationData):
    """Data of a :attr:`NotificationType.clash_invite` notification."""

    handle: str

    __slots__ = ("handle",)

    def __init__(self, state: "ConnectionState", data: types.ClashInviteData):
        self.handle = data["handle"]

        super().__init__(state, data)


class ClashOverData(NotificationData):
    """Data of a :attr:`NotificationType.clash_over` notification."""

    handle: str
    rank: int
    player_count: int

    __slots__ = (
        "handle",
        "rank",
        "player_count",
    )

    def __init__(self, state: "ConnectionState", data: types.ClashOverData):
        self.handle = data["handle"]
        self.rank = data["rank"]
        self.player_count = data["playerCount"]

        super().__init__(state, data)


# comment


class Contribution(Mapping):
    """Data about a contribution.

    This class has the same interface as :class:`dict` for backwards
    compatibility.
    """

    handle: str
    title: typing.Optional[str]
    type: typing.Optional[ContributionType]

    __slots__ = ("handle", "title", "type")

    def __init__(self, state: "ConnectionState", data: types.ContributionData):
        self.handle = data["handle"]
        self.title = data.get("title")
        self.type = ContributionType(data["type"]) if "type" in data else None

        super().__init__(state, data)


class PuzzleSolution(Mapping):
    """Data about a puzzle solution.

    This class has the same interface as :class:`dict` for backwards
    compatibility.
    """

    puzzle_id: str
    puzzle_url: typing.Optional[str]
    test_session_submission_id: int

    __slots__ = ("puzzle_id", "puzzle_url", "test_session_submission_id")

    def __init__(
        self, state: "ConnectionState", data: types.PuzzleSolutionData
    ):
        self.puzzle_id = data["puzzleId"]
        self.puzzle_url = (
            (state.http.BASE_URL + data["puzzleDetailsPageUrl"])
            if "puzzleDetailsPageUrl" in data
            else None
        )
        self.test_session_submission_id = data["testSessionSubmissionId"]

        super().__init__(state, data)


class NewCommentData(NotificationData):
    """Data of a :attr:`NotificationType.new_comment` and
    :attr:`NotificationType.new_comment_response` notifications."""

    type: LanguageMapping
    comment_type: typing.Optional[CommentType]
    type_data: typing.Union[Contribution, PuzzleSolution, None]
    url: typing.Optional[str]

    __slots__ = ("type", "comment_type", "type_data", "url")

    def __init__(self, state: "ConnectionState", data: types.NewCommentData):
        self.type = LanguageMapping(state, data["type"])
        self.comment_type = (
            CommentType(data["commentType"]) if "commentType" in data else None
        )
        self.type_data = None
        if "typeData" in data:
            self.type_data = (
                Contribution(state, data["typeData"])
                if self.comment_type == CommentType.contribution
                else PuzzleSolution(state, data["typeData"])
            )
        self.url = (
            (state.http.BASE_URL + data["url"]) if "url" in data else None
        )

        super().__init__(state, data)


# contribution


class ContributionData(Mapping):
    """Data of :attr:`NotificationType.contribution_received`,
    :attr:`NotificationType.contribution_accepted`,
    :attr:`NotificationType.contribution_refused` and
    :attr:`NotificationType.contribution_clash_mode_removed` notifications."""

    handle: str
    title: typing.Optional[str]
    type: typing.Optional[ContributionType]

    __slots__ = ("handle", "title", "type")

    def __init__(self, state: "ConnectionState", data: types.ContributionData):
        self.handle = data["handle"]
        self.title = data.get("title")
        self.type = ContributionType(data["type"]) if "type" in data else None

        super().__init__(state, data)


# feature


class FeatureData(NotificationData):
    """Data of a :attr:`NotificationType.feature` notification."""

    title: typing.Optional[LanguageMapping]
    description: LanguageMapping
    image_url: str
    url: str

    __slots__ = (
        "title",
        "description",
        "image_url",
        "url",
    )

    def __init__(self, state: "ConnectionState", data: types.FeatureData):
        self.title = (
            LanguageMapping(state, data["title"]) if "title" in data else None
        )
        self.description = LanguageMapping(state, data["description"])
        self.image_url = data["image-instant"]
        self.url = (
            data["url"]
            if re.match(r"https?://", data["url"])
            else (state.http.BASE_URL + data["url"])
        )

        super().__init__(state, data)


# hints


class NewHintData(NotificationData):
    """Data of a :attr:`NotificationType.new_hint` notification."""

    puzzle_title: LanguageMapping
    thumbnail_url: str
    test_session_handle: str

    __slots__ = (
        "puzzle_title",
        "thumbnail_url",
        "test_session_handle",
    )

    def __init__(self, state: "ConnectionState", data: types.NewHintData):
        self.puzzle_title = LanguageMapping(state, data["puzzleTitle"])
        self.thumbnail_url = state.http.get_file_url(
            data["thumbnailBinaryId"], format="notification_picture"
        )
        self.test_session_handle = data["testSessionHandle"]

        super().__init__(state, data)


# moderation


class ContributionModeratedData(NotificationData):
    """Data of a :attr:`NotificationType.contribution_moderated`
    notification."""

    action_type: ContributionModeratedActionType
    contribution: Contribution

    __slots__ = (
        "action_type",
        "contribution",
    )

    def __init__(
        self, state: "ConnectionState", data: types.ContributionModeratedData
    ):
        self.action_type = ContributionModeratedActionType(data["actionType"])
        self.contribution = Contribution(state, data["contribution"])

        super().__init__(state, data)


# puzzle


class NewPuzzleData(NotificationData):
    """Data of a :attr:`NotificationType.new_puzzle` notification."""

    level: LanguageMapping
    name: LanguageMapping
    image_url: str
    puzzle_id: int

    __slots__ = (
        "level",
        "name",
        "image_url",
        "puzzle_id",
    )

    def __init__(self, state: "ConnectionState", data: types.NewPuzzleData):
        self.level = LanguageMapping(state, data["level"])
        self.name = LanguageMapping(state, data["name"])
        self.image_url = data["image"]
        self.puzzle_id = data["puzzleId"]

        super().__init__(state, data)


class PuzzleOfTheWeekData(NotificationData):
    """Data of a :attr:`NotificationType.puzzle_of_the_week` notification."""

    puzzle_id: int
    puzzle_level: str
    puzzle_pretty_id: str
    puzzle_name: LanguageMapping
    puzzle_image_url: str
    contributor_pseudo: str
    contributor_avatar_url: typing.Optional[str]

    __slots__ = (
        "puzzle_id",
        "puzzle_level",
        "puzzle_pretty_id",
        "puzzle_name",
        "puzzle_image_url",
        "contributor_pseudo",
        "contributor_avatar_url",
    )

    def __init__(
        self, state: "ConnectionState", data: types.PuzzleOfTheWeekData
    ):
        self.puzzle_id = data["puzzleId"]
        self.puzzle_level = data["puzzleLevel"]
        self.puzzle_pretty_id = data["puzzlePrettyId"]
        self.puzzle_name = LanguageMapping(state, data["puzzleName"])
        self.puzzle_image_url = state.http.get_file_url(
            data["puzzleOfTheWeekImageId"], format="notification_picture"
        )
        self.contributor_pseudo = data["contributorNickname"]
        self.contributor_avatar_url = (
            state.http.get_file_url(
                data["contributorAvatarId"], format="notification_picture"
            )
            if "contributorAvatarId" in data
            else None
        )

        super().__init__(state, data)


# quest


class QuestCompletedData(NotificationData):
    """Data of a :attr:`NotificationType.quest_completed` notification."""

    id: int
    label: LanguageMapping

    __slots__ = (
        "id",
        "label",
    )

    def __init__(
        self, state: "ConnectionState", data: types.QuestCompletedData
    ):
        self.id = data["questId"]
        self.label = LanguageMapping(state, data["label"])

        super().__init__(state, data)


# social


class FriendRegisteredData(NotificationData):
    """Data of a :attr:`NotificationType.friend_registered` notification."""

    name: str

    __slots__ = ("name",)

    def __init__(
        self, state: "ConnectionState", data: types.FriendRegisteredData
    ):
        self.name = data["name"]

        super().__init__(state, data)


# xp


class NewLevelData(NotificationData):
    """Data of a :attr:`NotificationType.new_level` notification."""

    level: int
    reward: typing.Optional[LanguageMapping]
    trigger_career_popup: typing.Optional[bool]

    __slots__ = (
        "level",
        "reward",
        "trigger_career_popup",
    )

    def __init__(self, state: "ConnectionState", data: types.NewLevelData):
        self.level = data["level"]
        self.reward = (
            LanguageMapping(state, data["reward"]) if "reward" in data else None
        )
        self.trigger_career_popup = data.get("triggerCareerPopup")

        super().__init__(state, data)


# generic


class GenericData(NotificationData):
    """Data of a :attr:`NotificationType.info_generic`,
    :attr:`NotificationType.warning_generic` and
    :attr:`NotificationType.important_generic` notifications."""

    title: LanguageMapping
    description: LanguageMapping
    image_url: str
    url: str

    __slots__ = (
        "title",
        "description",
        "image_url",
        "url",
    )

    def __init__(self, state: "ConnectionState", data: types.GenericData):
        self.description = LanguageMapping(state, data["description"])
        self.url = data["url"]

        super().__init__(state, data)


# custom


class CustomData(NotificationData):
    """Data of a :attr:`NotificationType.custom` notification."""

    title: LanguageMapping
    description: LanguageMapping
    image_url: str
    url: str

    __slots__ = (
        "title",
        "description",
        "image_url",
        "url",
    )

    def __init__(self, state: "ConnectionState", data: types.CustomData):
        self.title = LanguageMapping(state, data["title"])
        self.description = LanguageMapping(state, data["description"])
        self.image_url = state.http.STATIC_URL + data["image"]
        self.url = (
            (state.http.BASE_URL + data["url"])
            if data["url"].startswith("/")
            else data["url"]
        )

        super().__init__(state, data)


# other


class CareerCandidateData(NotificationData):
    """Data of a :attr:`NotificationType.career_new_candidate` and
    :attr:`NotificationType.career_update_candidate` notifications."""

    handle: str
    username: typing.Optional[str]
    country: str
    region: str
    avatar_url: typing.Optional[str]

    __slots__ = (
        "handle",
        "username",
        "country",
        "region",
        "avatar_url",
    )

    def __init__(
        self, state: "ConnectionState", data: types.CareerCandidateData
    ):
        self.handle = data["handle"]
        self.username = data.get("username")
        self.country = data["country"]
        self.region = data["region"]
        self.avatar_url = (
            state.http.get_file_url(
                data["avatar"], format="notification_picture"
            )
            if "avatar" in data
            else None
        )

        super().__init__(state, data)


# no category


class TestFinishedData(NotificationData):
    """Data of a :attr:`NotificationType.test_finished` notification."""

    campaign_id: int
    candidate_id: int
    candidate_name: typing.Optional[str]
    candidate_email: str

    __slots__ = (
        "campaign_id",
        "candidate_id",
        "candidate_name",
        "candidate_email",
    )

    def __init__(self, state: "ConnectionState", data: types.TestFinishedData):
        self.campaign_id = data["campaignId"]
        self.candidate_id = data["candidateId"]
        self.candidate_name = data.get("candidateName")
        self.candidate_email = data["candidateEmail"]

        super().__init__(state, data)


class JobAcceptedData(NotificationData):
    """Data of a :attr:`NotificationType.job_accepted` notification."""

    job_name: typing.Optional[str]
    job_offer_location: str
    challenge_id: typing.Optional[int]

    __slots__ = (
        "job_name",
        "job_offer_location",
        "challenge_id",
    )

    def __init__(self, state: "ConnectionState", data: types.JobAcceptedData):
        self.job_name = data.get("jobName")
        self.job_offer_location = data["jobOfferLocation"]
        self.challenge_id = data.get("challengeId")

        super().__init__(state, data)


class JobExpiredData(NotificationData):
    """Data of a :attr:`NotificationType.job_expired` notification."""

    job_name: typing.Optional[str]

    __slots__ = ("job_name",)

    def __init__(self, state: "ConnectionState", data: types.JobExpiredData):
        self.job_name = data.get("jobName")

        super().__init__(state, data)


class NewWorkBlogData(NotificationData):
    """Data of a :attr:`NotificationType.new_work_blog` notification."""

    title: LanguageMapping
    url: LanguageMapping

    __slots__ = (
        "title",
        "url",
    )

    def __init__(self, state: "ConnectionState", data: types.NewWorkBlogData):
        self.title = LanguageMapping(state, data["title"])
        self.url = LanguageMapping(
            state,
            {
                lang: state.http.BASE_URL + path
                for lang, path in data["url"].items()
            },
        )

        super().__init__(state, data)


class OfferApplyData(NotificationData):
    """Data of a :attr:`NotificationType.offer_apply` notification."""

    candidate_name: str
    job_name: typing.Optional[str]
    job_offer_location: str
    challenge_id: typing.Optional[int]
    job_offer_id: typing.Optional[int]
    job_offer_applicant_id: typing.Optional[int]

    __slots__ = (
        "candidate_name",
        "job_name",
        "job_offer_location",
        "challenge_id",
        "job_offer_id",
        "job_offer_applicant_id",
    )

    def __init__(self, state: "ConnectionState", data: types.OfferApplyData):
        self.candidate_name = data["candidateName"]
        self.job_name = data.get("jobName")
        self.job_offer_location = data["jobOfferLocation"]
        self.challenge_id = data.get("challengeId")
        self.job_offer_id = data.get("jobOfferId")
        self.job_offer_applicant_id = data.get("jobOfferApplicantId")

        super().__init__(state, data)
