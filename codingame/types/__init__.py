"""
codingame.types
~~~~~~~~~~~~~~~
Typings for the CodinGame API.
"""

from .clash_of_code import ClashOfCode, Player
from .codingamer import (
    CodinGamerFromHandle,
    CodinGamerFromID,
    Follower,
    Following,
    PartialCodinGamer,
    PointsStatsFromHandle,
)
from .notification import (
    Notification,
    NotificationData,
    NotificationType,
    NotificationTypeGroup,
)

__all__ = (
    # codingamer
    PartialCodinGamer,
    CodinGamerFromID,
    CodinGamerFromHandle,
    PointsStatsFromHandle,
    Follower,
    Following,
    # clash of code
    ClashOfCode,
    Player,
    # notification
    Notification,
    NotificationData,
    NotificationType,
    NotificationTypeGroup,
)
