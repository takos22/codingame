from abc import ABC, abstractmethod

from ..endpoints import Endpoints

__all__ = ("BaseHTTPClient",)


class BaseHTTPClient(ABC):
    headers: dict = {
        "User-Agent": (
            "CodinGame API wrapper in Python "
            "(https://github.com/takos22/codingame)"
        )
    }

    @property
    def is_async(self):
        return False

    @abstractmethod
    def close(self):
        ...  # pragma: no cover

    @abstractmethod
    def request(self, url: str, json: list = []):
        ...  # pragma: no cover

    def login(self, email: str, password: str):
        return self.request(Endpoints.login, [email, password, True])

    def search(self, query: str):
        return self.request(Endpoints.search, [query, "en", None])

    def get_codingamer_from_handle(self, handle: str):
        return self.request(Endpoints.codingamer_from_handle, [handle])

    def get_codingamer_from_id(self, id: int):
        return self.request(Endpoints.codingamer_from_id, [id])

    def get_codingamer_followers(self, id: int):
        return self.request(Endpoints.codingamer_followers, [id, id, None])

    def get_codingamer_follower_ids(self, id: int):
        return self.request(Endpoints.codingamer_followers_ids, [id])

    def get_codingamer_following(self, id: int):
        return self.request(Endpoints.codingamer_following, [id, id])

    def get_codingamer_following_ids(self, id: int):
        return self.request(Endpoints.codingamer_following_ids, [id])

    def get_codingamer_clash_of_code_rank(self, id: int):
        return self.request(Endpoints.codingamer_clash_of_code_rank, [id])

    def get_clash_of_code_from_handle(self, handle: str):
        return self.request(Endpoints.clash_of_code, [handle])

    def get_pending_clash_of_code(self):
        return self.request(Endpoints.clash_of_code_pending)

    def get_language_ids(self):
        return self.request(Endpoints.language_ids)

    def get_unseen_notifications(self, id: int):
        return self.request(Endpoints.unseen_notifications, [id])

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
            Endpoints.global_leaderboard,
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
            Endpoints.challenge_leaderboard,
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
            Endpoints.puzzle_leaderboard,
            [puzzle_id, handle, group, filter],
        )
