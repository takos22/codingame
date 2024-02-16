import re
import typing
from datetime import datetime, timezone

from .exceptions import LoginRequired

__all__ = (
    "CODINGAMER_HANDLE_REGEX",
    "CLASH_OF_CODE_HANDLE_REGEX",
    "validate_leaderboard_type",
    "validate_leaderboard_group",
    "DT_FORMAT_1",
    "DT_FORMAT_2",
    "to_datetime",
)

CODINGAMER_HANDLE_REGEX = re.compile(r"[0-9a-f]{32}[0-9]{7}")
CLASH_OF_CODE_HANDLE_REGEX = re.compile(r"[0-9]{7}[0-9a-f]{32}")


def validate_leaderboard_type(type: str) -> str:
    """Validates that the leaderboard type is one of ``"GENERAL"``,
    ``"CONTESTS"``, ``"BOT_PROGRAMMING"``, ``"OPTIM"`` or ``"CODEGOLF"``.

    Parameters
    ----------
        type : :class:`str`
            The type to validate.

    Returns
    -------
        :class:`str`
            The valid type.

    Raises
    ------
        ValueError
            The type is invalid.
    """

    type = type.upper()
    if type not in [
        "GENERAL",
        "CONTESTS",
        "BOT_PROGRAMMING",
        "OPTIM",
        "CODEGOLF",
    ]:
        raise ValueError(
            "type argument must be one of: GENERAL, CONTESTS, "
            f"BOT_PROGRAMMING, OPTIM, CODEGOLF. Got: {type}"
        )

    return type


def validate_leaderboard_group(group: str, logged_in: bool) -> str:
    """Validates that the leaderboard group is one of ``"global"``,
    ``"country"``, ``"company"``, ``"school"`` or ``"following"`` and that the
    user is logged in except for ``"global"``.

    Parameters
    ----------
        type : :class:`str`
            The type to validate.
        logged_in : :class:`bool`
            Whether the user is logged in.

    Returns
    -------
        :class:`str`
            The valid group.

    Raises
    ------
        ValueError
            The group is invalid.
    """

    group = group.lower()
    if group not in [
        "global",
        "country",
        "company",
        "school",
        "following",
    ]:
        raise ValueError(
            "group argument must be one of: global, country, company, "
            f"school, following. Got: {group}"
        )

    if group in ["country", "company", "school", "following"] and not logged_in:
        raise LoginRequired()

    return group


DT_FORMAT_1 = "%b %d, %Y %I:%M:%S %p"
DT_FORMAT_2 = "%b %d, %Y, %I:%M:%S %p"  # see issue #23


def to_datetime(data: typing.Optional[typing.Union[int, str]]) -> datetime:
    if isinstance(data, int):
        return datetime.fromtimestamp(data / 1000.0, timezone.utc)
    elif isinstance(data, str):  # pragma: no cover
        try:
            return datetime.strptime(data, DT_FORMAT_1)
        except ValueError:
            return datetime.strptime(data, DT_FORMAT_2)
    elif data is None:
        return None
    else:
        raise TypeError  # pragma: no cover
