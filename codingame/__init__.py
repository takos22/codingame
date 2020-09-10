"""
CodinGame API Wrapper
~~~~~~~~~~~~~~~~~~~~~

Basic wrapper for the undocumented CodinGame API.
"""

__title__ = 'codingame'
__author__ = 'takos22'
__version__ = '0.0.1'

__all__ = [
    "Client",
    "CodinGamer",
]

from .client import Client
from .codingamer import CodinGamer
