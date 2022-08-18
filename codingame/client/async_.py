import typing
from datetime import datetime

from ..clash_of_code import ClashOfCode
from ..codingamer import CodinGamer
from ..exceptions import LoginError, LoginRequired, NotFound
from ..http import HTTPError
from ..leaderboard import (
    ChallengeLeaderboard,
    GlobalLeaderboard,
    PuzzleLeaderboard,
)
from ..notification import Notification
from ..utils import (
    CLASH_OF_CODE_HANDLE_REGEX,
    CODINGAMER_HANDLE_REGEX,
    to_datetime,
    validate_leaderboard_group,
    validate_leaderboard_type,
)
from .base import BaseClient

__all__ = ("AsyncClient",)


class AsyncClient(BaseClient, doc_prefix="|coro|"):
    """Asynchronous client for the CodinGame API."""

    def __init__(self):
        super().__init__(is_async=True)

    async def close(self):
        await self._state.http.close()

    # --------------------------------------------------------------------------
    # CodinGamer

    async def login(
        self,
        email: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        remember_me_cookie: typing.Optional[str] = None,
    ) -> typing.Optional[CodinGamer]:
        if remember_me_cookie is not None:
            # see issue #5
            self._state.http.set_cookie("rememberMe", remember_me_cookie)
            self._state.logged_in = True

            codingamer_id = int(remember_me_cookie[:7])
            self._state.codingamer = await self.get_codingamer(codingamer_id)

            return self._state.codingamer
        else:
            raise LoginError(
                "Email/password login is unavailable, use cookie authentication"
                " instead, with the ``remember_me_cookie`` parameter."
            )

        # try:
        #     data = await self._state.http.login(email, password)
        # except HTTPError as error:
        #     raise LoginError.from_id(
        #         error.data["id"], error.data["message"]
        #     ) from None

        # self._state.logged_in = True
        # self._state.codingamer = CodinGamer(self._state, data["codinGamer"])
        # return self.codingamer

    async def get_codingamer(
        self, codingamer: typing.Union[str, int]
    ) -> CodinGamer:
        handle = None

        if isinstance(codingamer, int):
            try:
                data = await self._state.http.get_codingamer_from_id(codingamer)
            except HTTPError as error:
                if error.data["id"] == 404:
                    raise NotFound.from_type(
                        "codingamer", f"No CodinGamer with id {codingamer!r}"
                    ) from None
                raise  # pragma: no cover
            handle = data["publicHandle"]

        else:
            if CODINGAMER_HANDLE_REGEX.match(codingamer):
                handle = codingamer
            else:
                results = await self._state.http.search(codingamer)
                users = [
                    result for result in results if result["type"] == "USER"
                ]
                if users:
                    handle = users[0]["id"]
                else:
                    raise NotFound.from_type(
                        "codingamer",
                        f"No CodinGamer with username {codingamer!r}",
                    )

        data = await self._state.http.get_codingamer_from_handle(handle)
        if data is None:
            raise NotFound.from_type(
                "codingamer", f"No CodinGamer with handle {handle!r}"
            )
        return CodinGamer(self._state, data["codingamer"])

    # --------------------------------------------------------------------------
    # Clash of Code

    async def get_clash_of_code(self, handle: str) -> ClashOfCode:
        if not CLASH_OF_CODE_HANDLE_REGEX.match(handle):
            raise ValueError(
                f"Clash of Code handle {handle!r} isn't in the good format "
                "(regex: [0-9]{7}[0-9a-f]{32})."
            )

        try:
            data = await self._state.http.get_clash_of_code_from_handle(handle)
        except HTTPError as error:
            if error.data["id"] == 502:
                raise NotFound.from_type(
                    "clash_of_code", f"No Clash of Code with handle {handle!r}"
                ) from None
            raise  # pragma: no cover
        return ClashOfCode(self._state, data)

    async def get_pending_clash_of_code(self) -> typing.Optional[ClashOfCode]:
        data: list = await self._state.http.get_pending_clash_of_code()
        if len(data) == 0:
            return None  # pragma: no cover
        return ClashOfCode(self._state, data[0])  # pragma: no cover

    # --------------------------------------------------------------------------
    # Language IDs

    async def get_language_ids(self) -> typing.List[str]:
        return await self._state.http.get_language_ids()

    # --------------------------------------------------------------------------
    # Notifications

    async def get_unseen_notifications(self) -> typing.Iterator[Notification]:
        if not self.logged_in:
            raise LoginRequired()

        try:
            data = await self._state.http.get_unseen_notifications(
                self.codingamer.id
            )
        except HTTPError as error:
            if error.data["id"] == 492:
                raise LoginRequired() from None
            raise  # pragma: no cover

        for notification in data:
            yield Notification(self._state, notification)

    async def get_unread_notifications(self) -> typing.Iterator[Notification]:
        if not self.logged_in:
            raise LoginRequired()

        try:
            data = await self._state.http.get_unread_notifications(
                self.codingamer.id
            )
        except HTTPError as error:
            if error.data["id"] == 492:
                raise LoginRequired() from None
            raise  # pragma: no cover

        for notification in data:
            yield Notification(self._state, notification)

    async def get_read_notifications(self) -> typing.Iterator[Notification]:
        if not self.logged_in:
            raise LoginRequired()

        try:
            data = await self._state.http.get_last_read_notifications(
                self.codingamer.id
            )
        except HTTPError as error:
            if error.data["id"] == 492:
                raise LoginRequired() from None
            raise  # pragma: no cover

        for notification in data:
            yield Notification(self._state, notification)

    async def mark_notifications_as_seen(
        self, notifications: typing.List[typing.Union["Notification", int]]
    ) -> datetime:
        if not notifications:
            raise ValueError("notifications argument must not be empty.")

        if not self.logged_in:
            raise LoginRequired()

        try:
            data = await self._state.http.mark_notifications_as_seen(
                self.codingamer.id,
                [n if isinstance(n, int) else n.id for n in notifications],
            )
        except HTTPError as error:
            if error.data["id"] == 492:
                raise LoginRequired() from None
            raise  # pragma: no cover

        seen_date = to_datetime(data)
        for notification in notifications:
            if isinstance(notification, int):
                continue
            notification._setattr("seen", True)
            notification._setattr("seen_date", seen_date)

        return seen_date

    async def mark_notifications_as_read(
        self, notifications: typing.List[typing.Union["Notification", int]]
    ) -> datetime:
        if not notifications:
            raise ValueError("notifications argument must not be empty.")

        if not self.logged_in:
            raise LoginRequired()

        try:
            data = await self._state.http.mark_notifications_as_read(
                self.codingamer.id,
                [n if isinstance(n, int) else n.id for n in notifications],
            )
        except HTTPError as error:
            if error.data["id"] == 492:
                raise LoginRequired() from None
            raise  # pragma: no cover

        read_date = to_datetime(data)
        for notification in notifications:
            if isinstance(notification, int):
                continue
            notification._setattr("read", True)
            notification._setattr("read_date", read_date)

        return read_date

    # --------------------------------------------------------------------------
    # Leaderboards

    async def get_global_leaderboard(
        self, page: int = 1, type: str = "GENERAL", group: str = "global"
    ) -> GlobalLeaderboard:
        type = validate_leaderboard_type(type)
        group = validate_leaderboard_group(group, self.logged_in)

        data = await self._state.http.get_global_leaderboard(
            page,
            type,
            group,
            self.codingamer.public_handle if self.logged_in else "",
        )
        return GlobalLeaderboard(self._state, type, group, page, data)

    async def get_challenge_leaderboard(
        self, challenge_id: str, group: str = "global"
    ) -> ChallengeLeaderboard:
        group = validate_leaderboard_group(group, self.logged_in)

        try:
            data = await self._state.http.get_challenge_leaderboard(
                challenge_id,
                group,
                self.codingamer.public_handle if self.logged_in else "",
            )
        except HTTPError as error:
            if error.data["id"] == 702:
                raise NotFound.from_type(
                    "challenge", f"No Challenge named {challenge_id!r}"
                ) from None
            raise  # pragma: no cover

        return ChallengeLeaderboard(self._state, challenge_id, group, data)

    async def get_puzzle_leaderboard(
        self, puzzle_id: str, group: str = "global"
    ) -> PuzzleLeaderboard:
        group = validate_leaderboard_group(group, self.logged_in)

        try:
            data = await self._state.http.get_puzzle_leaderboard(
                puzzle_id,
                group,
                self.codingamer.public_handle if self.logged_in else "",
            )
        except HTTPError as error:
            if error.data["code"] == "INVALID_PARAMETERS":
                raise NotFound.from_type(
                    "puzzle", f"No Puzzle named {puzzle_id!r}"
                ) from None
            raise  # pragma: no cover

        return PuzzleLeaderboard(self._state, puzzle_id, group, data)
