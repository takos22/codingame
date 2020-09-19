"""Abstract Base Classes"""

import abc
from typing import Optional

from .endpoints import Endpoints

class BaseUser(abc.ABC):
    """ABC for codingame users (CodinGamer, Player, ...)

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the User (hexadecimal str).

        id: :class:`int`
            ID of the User. Last 7 digits of the :attr:`public_handle` reversed.

        avatar: Optional[:class:`int`]
            Avatar ID of the User, if set else `None`. You can get the avatar url with :attr:`avatar_url`.

        cover: Optional[:class:`int`]
            Cover ID of the User, if set else `None`. You can get the cover url with :attr:`cover_url`.

    """

    public_handle: str
    id: int
    avatar: Optional[int] = None
    cover: Optional[int] = None

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Avatar URL of the User, if set else `None`."""
        return Endpoints.image.format(self.avatar) if self.avatar else None

    @property
    def cover_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Cover URL of the User, if set else `None`."""
        return Endpoints.image.format(self.cover) if self.cover else None

    def __repr__(self):
        return "<{0.__class__.__name__} public_handle={0.public_handle!r} id={0.id}>".format(self)

    def __eq__(self, other):
        return self.public_handle == other.public_handle
