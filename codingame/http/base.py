import typing
from abc import ABC, abstractmethod

from ..types import (
    ClashOfCode,
    CodinGamerFromID,
    Follower,
    Following,
    Notification,
    PointsStatsFromHandle,
)

if typing.TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("BaseHTTPClient",)


class BaseHTTPClient(ABC):
    BASE_URL = "https://www.codingame.com"
    API_URL = BASE_URL + "/services/"
    STATIC_URL = "https://static.codingame.com"

    headers: dict = {
        "User-Agent": (
            "CodinGame API wrapper in Python "
            "(https://github.com/takos22/codingame)"
        )
    }
    state: "ConnectionState"

    @property
    @abstractmethod
    def is_async(self) -> bool:
        ...  # pragma: no cover

    @abstractmethod
    def close(self):
        ...  # pragma: no cover

    @abstractmethod
    def request(self, service: str, func: str, parameters: list = []):
        ...  # pragma: no cover

    @abstractmethod
    def set_cookie(
        self,
        name: str,
        value: typing.Optional[str] = None,
        domain: str = "www.codingame.com",
    ):
        ...  # pragma: no cover

    def get_file_url(self, id: int, format: str = None) -> str:
        url = f"{self.STATIC_URL}/servlet/fileservlet?id={id}"
        if format:
            url += f"&format={format}"
        return url

    # Search

    def search(self, query: str):
        return self.request("Search", "search", [query, "en", None])

    # ProgrammingLanguage

    def get_language_ids(self) -> typing.List[str]:
        return self.request("ProgrammingLanguage", "findAllIds")

    # CodinGamer

    def login(self, email: str, password: str):  # pragma: no cover
        return self.request(
            "CodinGamer", "loginSite", [email, password, True, "CODINGAME", ""]
        )

    def get_codingamer_from_handle(self, handle: str) -> PointsStatsFromHandle:
        return self.request(
            "CodinGamer", "findCodingamePointsStatsByHandle", [handle]
        )

    def get_codingamer_from_id(self, id: int) -> CodinGamerFromID:
        return self.request(
            "CodinGamer", "findCodinGamerPublicInformations", [id]
        )

    def get_codingamer_followers(
        self, id: int, current_id: int = None
    ) -> typing.List[Follower]:
        return self.request(
            "CodinGamer", "findFollowers", [id, current_id or id, None]
        )

    def get_codingamer_follower_ids(self, id: int) -> typing.List[int]:
        return self.request("CodinGamer", "findFollowerIds", [id])

    def get_codingamer_following(
        self, id: int, current_id: int = None
    ) -> typing.List[Following]:
        return self.request(
            "CodinGamer", "findFollowing", [id, current_id or id]
        )

    def get_codingamer_following_ids(self, id: int) -> typing.List[int]:
        return self.request("CodinGamer", "findFollowingIds", [id])

    # ClashOfCode

    def get_codingamer_clash_of_code_rank(self, id: int) -> int:
        return self.request("ClashOfCode", "getClashRankByCodinGamerId", [id])

    def get_clash_of_code_from_handle(self, handle: str) -> ClashOfCode:
        return self.request("ClashOfCode", "findClashByHandle", [handle])

    def get_pending_clash_of_code(self) -> typing.List[ClashOfCode]:
        return self.request("ClashOfCode", "findPendingClashes")

    # Notification

    def get_unread_notifications(self, id: int) -> typing.List[Notification]:
        return self.request("Notification", "findUnreadNotifications", [id])

    def get_unseen_notifications(self, id: int) -> typing.List[Notification]:
        return self.request("Notification", "findUnseenNotifications", [id])

    def get_last_read_notifications(self, id: int) -> typing.List[Notification]:
        return self.request(
            "Notification", "findLastReadNotifications", [id, None]
        )

    def mark_notifications_as_seen(
        self, id: int, notification_ids: typing.List[int]
    ) -> int:
        return self.request(
            "Notification", "markAsSeen", [id, notification_ids]
        )

    def mark_notifications_as_read(
        self, id: int, notification_ids: typing.List[int]
    ) -> int:
        return self.request(
            "Notification", "markAsRead", [id, notification_ids]
        )

    # Leaderboards

    def get_global_leaderboard(
        self,
        page: int,
        type: str,
        group: str,
        handle: str = "",
        filter: dict = {
            "active": False,
            "keyword": "",
            "column": "",
            "filter": "",
        },
    ):
        return self.request(
            "Leaderboards",
            "getGlobalLeaderboard",
            [page, type, filter, handle, True, group],
        )

    def get_challenge_leaderboard(
        self,
        challenge_id: str,
        group: str,
        handle: str = "",
        filter: dict = {
            "active": False,
            "keyword": "",
            "column": "",
            "filter": "",
        },
    ):
        return self.request(
            "Leaderboards",
            "getFilteredChallengeLeaderboard",
            [challenge_id, handle, group, filter],
        )

    def get_puzzle_leaderboard(
        self,
        puzzle_id: str,
        group: str,
        handle: str = "",
        filter: dict = {
            "active": False,
            "keyword": "",
            "column": "",
            "filter": "",
        },
    ):
        return self.request(
            "Leaderboards",
            "getFilteredPuzzleLeaderboard",
            [puzzle_id, handle, group, filter],
        )
