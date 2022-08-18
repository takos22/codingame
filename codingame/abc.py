"""Abstract Base Classes"""

import abc
import typing
from collections.abc import Mapping as BaseMapping

if typing.TYPE_CHECKING:
    from .state import ConnectionState

__all__ = (
    "BaseObject",
    "BaseUser",
)


class BaseObject(abc.ABC):
    """Abstract base class for any object returned by the CodinGame API.

    This makes all the attributes read-only."""

    _state: "ConnectionState"

    __slots__ = ("_state", "__initialised")

    def __init__(self, state: "ConnectionState"):
        self._state = state
        self.__initialised = True

    def __setattr__(self, name, value):
        if not name.startswith("_") and getattr(
            self, "_BaseObject__initialised", False
        ):  # pragma: no cover
            raise AttributeError(f"{name!r} attribute is read-only.")
        object.__setattr__(self, name, value)

    def _setattr(self, name: str, value):
        """Set the value of a read-only attribute."""

        object.__setattr__(self, name, value)


class BaseUser(BaseObject):
    """Abstract Base Class for codingame users (CodinGamer, Player, ...)."""

    public_handle: str
    """Public handle of the CodinGamer (hexadecimal str)."""
    id: int
    """ID of the CodinGamer. Last 7 digits of the :attr:`public_handle`
    reversed."""
    pseudo: typing.Optional[str]
    """Pseudo of the CodinGamer."""
    avatar: typing.Optional[int]
    """Avatar ID of the CodinGamer. You can get the avatar url with
    :attr:`avatar_url`."""
    cover: typing.Optional[int]
    """Cover ID of the CodinGamer. You can get the cover url with
    :attr:`cover_url`."""

    __slots__ = ("public_handle", "id", "pseudo", "avatar", "cover")

    @property
    def avatar_url(self) -> typing.Optional[str]:
        """Optional :class:`str`: Avatar URL of the CodinGamer."""
        return (
            self._state.http.get_file_url(self.avatar) if self.avatar else None
        )

    @property
    def cover_url(self) -> typing.Optional[str]:
        """Optional :class:`str`: Cover URL of the CodinGamer."""
        return self._state.http.get_file_url(self.cover) if self.cover else None

    def __repr__(self):
        return (
            "<{0.__class__.__name__} id={0.id!r} pseudo={0.pseudo!r}>".format(
                self
            )
        )

    def __eq__(self, other):
        return self.public_handle == other.public_handle


class Mapping(BaseMapping, BaseObject):
    _raw: dict

    __slots__ = ("_raw",)

    def __init__(self, state: "ConnectionState", data: dict):
        self._raw = data

        super().__init__(state)

    def __getitem__(self, name: str):  # pragma: no cover
        return self._raw[name]

    def __iter__(self):  # pragma: no cover
        return iter(self._raw)

    def __len__(self):  # pragma: no cover
        return len(self._raw)
