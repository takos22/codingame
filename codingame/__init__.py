"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

__title__ = 'codingame'
__author__ = 'takos22'
__version__ = '0.0.1a'

__all__ = [
    "Client",
    "CodinGamer",
]

from collections import namedtuple

from .client import Client
from .codingamer import CodinGamer

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)
