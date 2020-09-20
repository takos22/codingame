"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=3, micro=0, releaselevel=".post", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "0.3.0.post0"

__all__ = [
    "Client",
    "CodinGamer",
    "ClashOfCode",
    "Player",
    "CodinGameAPIError",
    "CodinGamerNotFound",
    "ClashOfCodeNotFound",
]

from .client import Client
from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode, Player
from .exceptions import CodinGameAPIError, CodinGamerNotFound, ClashOfCodeNotFound
