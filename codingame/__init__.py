"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=3, micro=2, releaselevel="", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "0.3.2"

__all__ = [
    "Client",
    "CodinGamer",
    "ClashOfCode",
    "Player",
    "Notification",
    "CodinGameAPIError",
    "CodinGamerNotFound",
    "ClashOfCodeNotFound",
    "LoginRequired",
]

from .client import Client
from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode, Player
from .notification import Notification
from .exceptions import CodinGameAPIError, CodinGamerNotFound, ClashOfCodeNotFound, LoginRequired
