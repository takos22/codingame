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
)

__all__ = (
    # codingamer
    CodinGamerFromID,
    CodinGamerFromHandle,
    Follower,
    Following,
    # clash of code
    ClashOfCode,
    Player,
)
