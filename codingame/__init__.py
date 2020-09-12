"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=2, micro=0, releaselevel="alpha", serial=0)

__title__ = "codingame"
__author__ = "takos22"
__version__ = "0.2.0a"

__all__ = [
    "Client",
    "CodinGamer",
    "ClashOfCode",
    "CodinGameAPIError",
    "CodinGamerNotFound",
    "ClashOfCodeNotFound",
]

from .client import Client
from .codingamer import CodinGamer
from .clash_of_code import ClashOfCode
from .exceptions import CodinGameAPIError, CodinGamerNotFound, ClashOfCodeNotFound
