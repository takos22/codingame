"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "0.1.0"

__all__ = [
    "Client",
    "CodinGamer",
    "CodinGameAPIError",
    "CodinGamerNotFound",
]

from .client import Client
from .codingamer import CodinGamer
from .exceptions import CodinGameAPIError, CodinGamerNotFound
