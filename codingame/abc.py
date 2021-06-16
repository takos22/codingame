"""Abstract Base Classes"""

import abc
from typing import Optional

from .endpoints import Endpoints


class BaseUser(abc.ABC):
    """Abstract Base Class for codingame users (CodinGamer, Player, ...)."""

    public_handle: str
    """Public handle of the CodinGamer (hexadecimal str)."""
    id: int
    """ID of the CodinGamer. Last 7 digits of the :attr:`public_handle`
    reversed."""
    pseudo: Optional[str]
    """Pseudo of the CodinGamer."""
    avatar: Optional[int]
    """Avatar ID of the CodinGamer. You can get the avatar url with
    :attr:`avatar_url`."""
    cover: Optional[int]
    """Cover ID of the CodinGamer. You can get the cover url with
    :attr:`cover_url`."""

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Avatar URL of the CodinGamer."""
        return Endpoints.image.format(self.avatar) if self.avatar else None

    @property
    def cover_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Cover URL of the CodinGamer."""
        return Endpoints.image.format(self.cover) if self.cover else None

    def __repr__(self):
        return (
            "<{0.__class__.__name__} id={0.id!r} pseudo={0.pseudo!r}>".format(
                self
            )
        )

    def __eq__(self, other):
        return self.public_handle == other.public_handle
