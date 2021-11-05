import typing
from datetime import datetime

from ..abc import BaseObject
from ..codingamer import PartialCodinGamer
from ..types import notification as types
from ..utils import to_datetime
from .data import NotificationData
from .enums import NotificationType, NotificationTypeGroup

if typing.TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("Notification",)


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
        except ValueError:  # pragma: no cover
            self.type = data["type"]
            print(
                f"unknown notification type {self.type}, please report this at "
                "https://github.com/takos22/codingame/issues/new"
            )

        try:
            self.type_group = NotificationTypeGroup(data["typeGroup"])
        except ValueError:  # pragma: no cover
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

        self.data = NotificationData.from_type(
            self.type, state, data.get("data")
        )
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
