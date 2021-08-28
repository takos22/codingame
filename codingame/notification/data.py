import typing
from datetime import datetime

from ..abc import Mapping
from ..types import notification as types
from ..utils import to_datetime
from .enums import CommentType, ContributionType, NotificationType

if typing.TYPE_CHECKING:
    from ..state import ConnectionState


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
    ):
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
            NT.new_comment_response: NewCommentResponseData,
            NT.quest_completed: QuestCompletedData,
            NT.friend_registered: FriendRegisteredData,
            NT.new_level: NewLevelData,
        }
        return type_to_obj.get(type, cls)(state, data) if data else None


# achievement


class AchievementUnlockedData(NotificationData):
    """Data of a :attr:`NotificationType.achievement_unlocked` notification."""

    id: str
    label: LanguageMapping
    points: int
    level: str
    completion_time: datetime
    image_id: int

    __slots__ = (
        "id",
        "label",
        "points",
        "level",
        "completion_time",
        "image_id",
    )

    def __init__(
        self, state: "ConnectionState", data: types.AchievementUnlockedData
    ):
        self.id = data["id"]
        self.label = LanguageMapping(state, data["label"])
        self.points = data["points"]
        self.level = data["level"]
        self.completion_time = to_datetime(data["completionTime"])
        self.image_id = data["imageId"]

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
    thumbnail_binary_id: int
    test_session_handle: str

    __slots__ = (
        "title_label",
        "division_index",
        "division_count",
        "division_offset",
        "threshold_index",
        "thumbnail_binary_id",
        "test_session_handle",
    )

    def __init__(self, state: "ConnectionState", data: types.LeagueData):
        self.title_label = LanguageMapping(state, data["titleLabel"])
        self.division_index = data["divisionIndex"]
        self.division_count = data["divisionCount"]
        self.division_offset = data["divisionOffset"]
        self.threshold_index = data["thresholdIndex"]
        self.thumbnail_binary_id = data["thumbnailBinaryId"]
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
        self.puzzle_url = data.get("puzzleDetailsPageUrl")
        self.test_session_submission_id = data["testSessionSubmissionId"]

        super().__init__(state, data)


class NewCommentData(NotificationData):
    """Data of a :attr:`NotificationType.new_comment` notification."""

    type: LanguageMapping
    comment_type: typing.Optional[CommentType]
    type_data: typing.Union[Contribution, PuzzleSolution, None]
    url: typing.Optional[str]

    __slots__ = ("type", "comment_type", "type_data", "url")

    def __init__(self, state: "ConnectionState", data: types.NewCommentData):
        self.type = LanguageMapping(data["type"])
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
        self.url = data.get("url")

        super().__init__(state, data)


class NewCommentResponseData(NotificationData):
    """Data of a :attr:`NotificationType.new_comment_response` notification."""

    comment_type: typing.Optional[CommentType]
    type_data: typing.Union[Contribution, PuzzleSolution, None]
    url: typing.Optional[str]

    __slots__ = ("comment_type", "type_data", "url")

    def __init__(
        self, state: "ConnectionState", data: types.NewCommentResponseData
    ):
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
        self.url = data.get("url")

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
