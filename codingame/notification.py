import typing
from datetime import datetime
from enum import Enum

from .abc import BaseObject
from .codingamer import PartialCodinGamer
from .types.notification import Notification as NotificationDict
from .types.notification import NotificationData

if typing.TYPE_CHECKING:
    from .state import ConnectionState

__all__ = ("Notification",)


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

    def __init__(self, state: "ConnectionState", data: NotificationDict):
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
        self.date = datetime.utcfromtimestamp(data["date"] / 1000.0)
        self.creation_time = self.date
        self.priority = data["priority"]
        self.urgent = data["urgent"]

        self.seen = bool(data.get("seenDate"))
        self.seen_date = None
        if self.seen:
            self.seen_date = datetime.utcfromtimestamp(
                data["seenDate"] / 1000.0
            )

        self.read = bool(data.get("readDate"))
        self.read_date = None
        if self.read:
            self.read_date = datetime.utcfromtimestamp(
                data["readDate"] / 1000.0
            )

        self.data = data.get("data")
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
