from datetime import datetime


class Notification:
    """Represents a Notification.

    Do not create this class yourself. Only get it through :attr:`Client.notifications`.

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
    """

    id: int
    type: str  # TODO create notification type enum
    type_group: str
    creation_time: datetime
    priority: int
    urgent: bool
    data: dict

    def __init__(self, notification):
        self.id = notification["id"]
        self.type = notification["type"]
        self.type_group = notification["typeGroup"]
        self.creation_time = datetime.utcfromtimestamp(notification["date"] / 1000.0)
        self.priority = notification["priority"]
        self.urgent = notification["urgent"]
        self.data = notification.get("data", None)

    def __repr__(self):
        return (
            "<Notification id={0.id!r} type={0.type!r} date={0.date!r} priority={0.priority!r} "
            "urgent={0.urgent!r} data={0.data!r}>".format(self)
        )
