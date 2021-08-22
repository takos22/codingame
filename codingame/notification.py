import typing
from collections.abc import Mapping
from datetime import datetime
from enum import Enum

from .abc import BaseObject
from .codingamer import PartialCodinGamer
from .types import notification as types
from .utils import to_datetime

if typing.TYPE_CHECKING:
    from .state import ConnectionState

__all__ = (
    "Notification",
    "NotificationType",
    "NotificationTypeGroup",
    "NotificationData",
    # data classes
    "AchievementUnlockedData",
    "LeagueData",
    "NewBlogData",
    "ClashInviteData",
    "ClashOverData",
    "QuestCompletedData",
    "FriendRegisteredData",
    "NewLevelData",
)

# enums


class NotificationTypeGroup(str, Enum):
    """Enumeration for the :attr:`Notification.type_group`.

    .. warning::
        There might be some missing type groups.
    """

    achievement = "achievement"
    arena = "arena"
    blog = "blog"
    clash = "clash"
    comment = "comment"
    contest = "contest"
    contribution = "contribution"
    feature = "feature"
    hints = "hints"
    moderation = "moderation"
    puzzle = "puzzle"
    quest = "quest"
    social = "social"
    xp = "xp"
    generic = "generic"
    custom = "custom"
    other = "other"


class NotificationType(str, Enum):
    """Enumeration for the :attr:`Notification.type`."""

    # achievement
    achievement_unlocked = "achievement-unlocked"
    """When a new achievement is unlocked."""

    # arena
    new_league = "new-league"
    """When a new league is added to an arena.

    If the new league is higher than your current one, you will get demoted,
    otherwise your league will stay the same."""
    eligible_for_next_league = "eligible-for-next-league"
    """When you are better than the boss of your current league.

    This means you will be promoted soon."""
    promoted_league = "promoted-league"
    """When you are promoted to a higher league."""

    # blog
    new_blog = "new-blog"
    """When a new blog entry is created."""

    # clash
    clash_invite = "clash-invite"
    """When you are invited to a Clash of Code."""
    clash_over = "clash-over"
    """When a Clash of Code you participated in is over."""

    # comment
    new_comment = "new-comment"
    """When someone comments your contribution or your solution."""
    new_comment_response = "new-comment-response"
    """When someone replies to your commeny."""

    # contest
    contest_scheduled = "contest-scheduled"
    """When a contest is scheduled."""
    contest_soon = "contest-soon"
    """When a contest is starting soon."""
    contest_started = "contest-started"
    """When a contest has started."""
    contest_over = "contest-over"
    """When a contest is over."""

    # contribution
    contribution_received = "contribution-received"
    """When your contribution is received."""
    contribution_accepted = "contribution-accepted"
    """When your contribution is accepted."""
    contribution_refused = "contribution-refused"
    """When your contribution is refused."""
    contribution_clash_mode_removed = "contribution-clash-mode-removed"
    """When your contribution is modified."""

    # feature
    feature = "feature"
    """When a new feature is available on CodinGame."""

    # hints
    new_hint = "new-hint"
    """When a new hint is revealed."""

    # moderation
    contribution_moderated = "contribution-moderated"
    """When your contribution is validated or denied."""

    # puzzle
    new_puzzle = "new-puzzle"
    """When a new puzzle is available."""
    puzzle_of_the_week = "puzzle-of-the-week"
    """When the puzzle of the week is available."""
    new_league_opened = "new-league-opened"
    """When a new league is opened.

    I don't know why this isn't in :attr:`NotificationTypeGroup.arena` like
    :attr:`NotificationType.new_league`,
    :attr:`NotificationType.eligible_for_next_league` and
    :attr:`NotificationType.promoted_league`."""

    # quest
    quest_completed = "quest-completed"
    """When a quest is completed."""

    # social
    following = "following"
    """When a CodinGamer starts following you."""
    friend_registered = "friend-registered"
    """When a friend registers on CodinGame."""
    invitation_accepted = "invitation-accepted"
    """When a friend accepts your invitation and registers on CodinGame."""

    # xp
    new_level = "new-level"
    """When you reach a new level."""

    # generic
    info_generic = "info-generic"
    """When you get a generic information notification."""
    warning_generic = "warning-generic"
    """When you get a generic warning notification."""
    important_generic = "important-generic"
    """When you get a generic important notification."""

    # custom
    custom = "custom"
    """When you get a custom notification."""

    # other
    career_new_candidate = "career-new-candidate"
    career_update_candidate = "career-update-candidate"

    # didn't find a category
    test_finished = "test-finished"
    job_accepted = "job-accepted"
    job_expired = "job-expired"
    new_work_blog = "new-work-blog"
    offer_apply = "offer-apply"
    recruiter_contact = "recruiter-contact"


# data


class LanguageMapping(Mapping, BaseObject):
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

        super(BaseObject).__init__(state)

    def __getitem__(self, language: str) -> str:
        return {"en": self.en, "fr": self.fr}[language]

    def __iter__(self):
        return iter({"en": self.en, "fr": self.fr})

    def __len__(self):
        return 2

    # TODO implement state.current_language
    # def __str__(self) -> str:
    #     return super().__str__()


class NotificationData(Mapping, BaseObject):
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

    __slots__ = ("_raw",)

    def __init__(self, state: "ConnectionState", data: types.NotificationData):
        self._raw = data
        super(BaseObject).__init__(state)

    def __getitem__(self, name: str):
        return self._raw[name]

    def __iter__(self):
        return iter(self._raw)

    def __len__(self):
        return len(self._raw)

    @classmethod
    def from_type(cls, type: NotificationType, data: types.NotificationData):
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
            NT.quest_completed: QuestCompletedData,
            NT.friend_registered: FriendRegisteredData,
            NT.new_level: NewLevelData,
        }
        return type_to_obj.get(type, cls) if data else None


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


# notification


class Notification(BaseObject):
    """Represents a Notification.

    Attributes
    -----------
        id: :class:`int`
            ID of the notification.

        type_group: :class:`NotificationTypeGroup`
            Group type of the notification.

        type: :class:`NotificationType`
            Precise type of the notification.

        date: :class:`~datetime.datetime`
            Date of the notification. Was ``notification.creation_time``.

        creation_time: :class:`~datetime.datetime`
            Date of the notification.

            .. deprecated:: 1.2
                Use :attr:`date` instead.

        priority: :class:`int`
            Priority of the notification.

        urgent: :class:`bool`
            Whether the notification is urgent.

        seen: :class:`bool`
            Whether the notification has been seen.

        seen_date: Optional :class:`~datetime.datetime`
            Date when the notification was seen.

        read: :class:`bool`
            Whether the notification has been read.

        read_date: Optional :class:`~datetime.datetime`
            Date when the notification was read.

        data: Optional :class:`dict`
            Data of the notification.

            .. note::
                Every notification type has different data.
                So there isn't the same keys and values every time.

        codingamer: Optional :class:`PartialCodinGamer`
            CodinGamer that sent the notification, only appears in some
            notification types.
    """

    id: int
    type: NotificationType
    type_group: NotificationTypeGroup
    date: datetime
    priority: int
    urgent: bool
    seen: bool
    seen_date: typing.Optional[datetime]
    read: bool
    read_date: typing.Optional[datetime]
    data: typing.Optional[NotificationData]
    codingamer: typing.Optional[PartialCodinGamer]

    __slots__ = (
        "id",
        "type",
        "type_group",
        "date",
        "creation_time",
        "priority",
        "urgent",
        "seen",
        "seen_date",
        "read",
        "read_date",
        "data",
        "codingamer",
    )

    def __init__(self, state: "ConnectionState", data: types.Notification):
        self.id = data["id"]
        try:
            self.type = NotificationType(data["type"])
        except ValueError:
            self.type = data["type"]
            print(
                f"unknown notification type {self.type}, please report this at "
                "https://github.com/takos22/codingame/issues/new"
            )

        try:
            self.type_group = NotificationTypeGroup(data["typeGroup"])
        except ValueError:
            self.type_group = data["typeGroup"]
            print(
                f"unknown notification type group {self.type_group}, please "
                "report this at https://github.com/takos22/codingame/issues/new"
            )

        self.date = to_datetime(data["date"])
        self.creation_time = self.date
        self.priority = data["priority"]
        self.urgent = data["urgent"]

        self.seen = bool(data.get("seenDate"))
        self.seen_date = None
        if self.seen:
            self.seen_date = to_datetime(data["seenDate"])

        self.read = bool(data.get("readDate"))
        self.read_date = None
        if self.read:
            self.read_date = to_datetime(data["readDate"])

        self.data = NotificationData.from_type(self.type, data.get("data"))
        self.codingamer = None
        if data.get("codingamer"):
            self.codingamer = PartialCodinGamer(state, data["codingamer"])

        super().__init__(state)

    def __repr__(self):
        return (
            "<Notification id={0.id!r} type={0.type!r} "
            "date={0.date!r} urgent={0.urgent!r} "
            "seen={0.seen!r} read={0.read!r}>"
        ).format(self)
