import typing

from .. import exceptions
from ..clash_of_code import ClashOfCode
from ..codingamer import CodinGamer
from ..http import HTTPError
from ..leaderboard import (
    ChallengeLeaderboard,
    GlobalLeaderboard,
    PuzzleLeaderboard,
)
from ..notification import Notification
from ..utils import CLASH_OF_CODE_HANDLE_REGEX, CODINGAMER_HANDLE_REGEX
from .base import BaseClient


class SyncClient(BaseClient):
    """CodinGame API client.

    Attributes
    -----------
        logged_in: :class:`bool`
            If the client is logged in as a CodinGamer.

        codingamer: Optional[:class:`CodinGamer`]
            The CodinGamer that is logged in through the client.
            ``None`` if the client isn't logged in.
    """

    def __init__(self):
        super().__init__(is_async=False)

    def login(self, email: str, password: str) -> CodinGamer:
        try:
            data = self._state.http.login(email, password)
        except HTTPError as error:
            raise exceptions.LoginError.from_id(
                error.data["id"], error.data["message"]
            ) from None

        self._state.logged_in = True
        self._state.codingamer = CodinGamer(self._state, data["codinGamer"])
        return self.codingamer

    def get_codingamer(self, codingamer: typing.Union[str, int]) -> CodinGamer:
        handle = None

        if isinstance(codingamer, int):
            try:
                data = self._state.http.get_codingamer_from_id(codingamer)
            except HTTPError as error:
                if error.data["id"] == 404:
                    raise exceptions.CodinGamerNotFound(
                        f"No CodinGamer with id {codingamer!r}"
                    ) from None
                raise  # pragma: no cover
            handle = data["publicHandle"]

        if handle is None and not CODINGAMER_HANDLE_REGEX.match(codingamer):
            results = self._state.http.search(codingamer)
            users = [result for result in results if result["type"] == "USER"]
            if users:
                handle = users[0]["id"]
            else:
                raise exceptions.CodinGamerNotFound(
                    f"No CodinGamer with username {codingamer!r}"
                )
        elif handle is None:
            handle = codingamer

        data = self._state.http.get_codingamer_from_handle(handle)
        if data is None:
            raise exceptions.CodinGamerNotFound(
                f"No CodinGamer with handle {handle!r}"
            )
        return CodinGamer(self._state, data["codingamer"])

    def get_clash_of_code(self, handle: str) -> ClashOfCode:
        if not CLASH_OF_CODE_HANDLE_REGEX.match(handle):
            raise ValueError(
                f"Clash of Code handle {handle!r} isn't in the good format "
                "(regex: [0-9]{7}[0-9a-f]{32})."
            )

        try:
            data = self._state.http.get_clash_of_code_from_handle(handle)
        except HTTPError as error:
            if error.data["id"] == 502:
                raise exceptions.ClashOfCodeNotFound(
                    f"No Clash of Code with handle {handle!r}"
                ) from None
            raise  # pragma: no cover
        return ClashOfCode(self._state, data)

    def get_pending_clash_of_code(self) -> typing.Optional[ClashOfCode]:

        data: list = self._state.http.get_pending_clash_of_code()
        if len(data) == 0:
            return None  # pragma: no cover
        return ClashOfCode(self._state, data[0])  # pragma: no cover

    def get_language_ids(self) -> typing.List[str]:
        return self._state.http.get_language_ids()

    def get_unseen_notifications(self) -> typing.Iterator[Notification]:

        if not self.logged_in:
            raise exceptions.LoginRequired()

        data = self._state.http.get_unseen_notifications(self.codingamer.id)
        for notification in data:
            yield Notification(self._state, notification)

    def get_global_leaderboard(
        self, page: int = 1, type: str = "GENERAL", group: str = "global"
    ) -> GlobalLeaderboard:
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

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise exceptions.LoginRequired()

        data = self._state.http.get_global_leaderboard(
            page,
            type,
            group,
            self.codingamer.public_handle if self.logged_in else "",
        )
        return GlobalLeaderboard(self._state, type, group, page, data)

    def get_challenge_leaderboard(
        self, challenge_id: str, group: str = "global"
    ) -> ChallengeLeaderboard:
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

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise exceptions.LoginRequired()

        try:
            data = self._state.http.get_challenge_leaderboard(
                challenge_id,
                group,
                self.codingamer.public_handle if self.logged_in else "",
            )
        except HTTPError as error:
            if error.data["id"] == 702:
                raise exceptions.ChallengeNotFound(
                    f"No Challenge named {challenge_id!r}"
                ) from None
            raise  # pragma: no cover

        return ChallengeLeaderboard(self._state, challenge_id, group, data)

    def get_puzzle_leaderboard(
        self, puzzle_id: str, group: str = "global"
    ) -> PuzzleLeaderboard:
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

        if (
            group in ["country", "company", "school", "following"]
            and not self.logged_in
        ):
            raise exceptions.LoginRequired()

        try:
            data = self._state.http.get_puzzle_leaderboard(
                puzzle_id,
                group,
                self.codingamer.public_handle if self.logged_in else "",
            )
        except HTTPError as error:
            if error.data["code"] == "INVALID_PARAMETERS":
                raise exceptions.PuzzleNotFound(
                    f"No Puzzle named {puzzle_id!r}"
                ) from None
            raise  # pragma: no cover

        return PuzzleLeaderboard(self._state, puzzle_id, group, data)