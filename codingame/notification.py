import typing
from datetime import datetime

from .abc import BaseObject

__all__ = ("Notification",)


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

        creation_time: :class:`datetime`
            Creation time of the notification.

        priority: :class:`int`
            Priority of the notification.

        urgent: :class:`bool`
            If the notification is urgent.

        data: :class:`dict`
            Data of the notification.

            .. note::
                Every notification type has different data.
                So there isn't the same keys and values every time.

        _raw: :class:`dict`
            The dict from CodinGame describing the notification.
            Useful when there's more data that isn't included in the normal
            fields.
    """

    id: int
    type: str  # TODO create notification type enum
    type_group: str
    creation_time: datetime
    priority: int
    urgent: bool
    data: typing.Optional[dict]
    _raw: dict

    __slots__ = (
        "id",
        "type",
        "type_group",
        "creation_time",
        "priority",
        "urgent",
        "data",
        "_raw",
    )

    def __init__(self, state, notification):
        self._state = state
        self._raw = notification  # for attributes that arent wrapped

        self.id = notification["id"]
        self.type = notification["type"]
        self.type_group = notification["typeGroup"]
        self.creation_time = datetime.utcfromtimestamp(
            notification["date"] / 1000.0
        )
        self.priority = notification["priority"]
        self.urgent = notification["urgent"]
        self.data = notification.get("data")

    def __repr__(self):
        return (
            "<Notification id={0.id!r} type={0.type!r} "
            "creation_time={0.creation_time!r} priority={0.priority!r} "
            "urgent={0.urgent!r}>".format(self)
        )
