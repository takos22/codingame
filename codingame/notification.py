from datetime import datetime


class Notification:

    id: int
    type: str
    type_group: str
    priority: int
    date: datetime
    urgent: bool
    label: str
    label_fr: str
    data: dict

    def __init__(self, notification):
        self.id = notification["id"]
        self.type = notification["type"]
        self.type_group = notification["typeGroup"]
        self.priority = notification["priority"]
        self.date = datetime.utcfromtimestamp(notification["date"] / 1000.0)
        self.urgent = notification["urgent"]
        self.data = notification.get("data", None)

    def __repr__(self):
        return (
            "<Notification id={0.id!r} type={0.type!r} date={0.date!r} priority={0.priority!r} "
            "urgent={0.urgent!r} data={0.data!r}>".format(self)
        )
