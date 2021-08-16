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
    ACHIEVEMENT = "achievement"
    ARENA = "arena"
    BLOG = "blog"
    CLASH = "clash"
    COMMENT = "comment"
    CONTEST = "contest"
    CONTRIBUTION = "contribution"
    FEATURE = "feature"
    HINTS = "hints"
    MODERATION = "moderation"
    PUZZLE = "puzzle"
    QUEST = "quest"
    SOCIAL = "social"
    XP = "xp"
    CUSTOM = "custom"
    OTHER = "other"


class Notification(BaseObject):
    """Represents a Notification.

    Attributes
    -----------
        id: :class:`int`
            ID of the notification.

        type_group: :class:`str`
            Group type of the notification.

        type: :class:`str`
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

        codingamer: Optional :class:`PartialCodingamer`
            CodinGamer that sent the notification, only appears in some
            notification types.
    """

    id: int
    type: str  # TODO create notification type enum
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
        self.type = data["type"]
        self.type_group = NotificationTypeGroup(data["typeGroup"])
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
