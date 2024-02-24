from datetime import datetime
from typing import TYPE_CHECKING

from ..abc import BaseObject
from ..codingamer import PartialCodinGamer
from ..utils import to_datetime

if TYPE_CHECKING:
    from ..state import ConnectionState
    from .clash_of_code import ClashOfCode


class Solution(BaseObject):
    clash_of_code: "ClashOfCode"
    codingamer: PartialCodinGamer
    submission_id: int
    commentable_id: int
    votable_id: int
    creation_time: datetime
    language_id: str
    code: str
    shared: bool

    __slots__ = (
        "clash_of_code",
        "codingamer",
        "codingamer",
        "submission_id",
        "commentable_id",
        "votable_id",
        "creation_time",
        "language_id",
        "code",
        "shared",
    )

    def __init__(
        self, state: "ConnectionState", clash_of_code: "ClashOfCode", data: dict
    ):
        self.clash_of_code = clash_of_code
        self.codingamer = PartialCodinGamer(
            state,
            dict(
                publicHandle=data["codingamerHandle"],
                userId=data["codingamerId"],
                pseudo=data.get("pseudo"),
                avatar=data.get("avatar"),
                cover=data.get("cover"),
            ),
        )

        self.submission_id = data["testSessionQuestionSubmissionId"]
        self.commentable_id = data["commentableId"]
        self.votable_id = data["votableId"]

        self.creation_time = to_datetime(data["creationTime"])
        self.language_id = data["programmingLanguageId"]
        self.code = data["code"]
        self.shared = data["shared"]

        super().__init__(state)

    def share(self):

        if self._state.is_async:

            async def _share():
                await self._state.http.share_clash_of_code_solution(
                    self._state.codingamer.id, self.clash_of_code.public_handle
                )
                self._setattr("shared", True)

        else:

            def _share():
                self._state.http.share_clash_of_code_solution(
                    self._state.codingamer.id, self.clash_of_code.public_handle
                )
                self._setattr("shared", True)

        return _share()
