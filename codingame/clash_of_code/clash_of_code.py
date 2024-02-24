from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Optional

from ..abc import BaseObject
from ..exceptions import ClashOfCodeError, LoginRequired
from ..http.httperror import HTTPError
from ..types.clash_of_code import ClashOfCode as ClashOfCodeDict
from ..types.clash_of_code import LanguageIds, Mode, Modes
from ..utils import minified_players_to_players, to_datetime
from .player import Player
from .question import Question, TestCaseResult
from .solution import Solution

if TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("ClashOfCode",)


class ClashOfCode(BaseObject):
    """Represents a Clash of Code.

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the Clash of Code (hexadecimal str).

        join_url: :class:`str`
            URL to join the Clash of Code.

        public: :class:`bool`
            Whether the Clash of Code is public.

        min_players: :class:`int`
            Minimum number of players.

        max_players: :class:`int`
            Maximum number of players.

        modes: Optional :class:`list` of :class:`str`
            List of possible modes.

        programming_languages: Optional :class:`list` of :class:`str`
            List of possible programming languages.

        started: :class:`bool`
            Whether the Clash of Code is started.

        finished: :class:`bool`
            Whether the Clash of Code is finished.

        mode: Optional :class:`str`
            The mode of the Clash of Code.

        creation_time: Optional :class:`~datetime.datetime`
            Creation time of the Clash of Code.
            Doesn't always exist.

        start_time: :class:`~datetime.datetime`
            Start time of the Clash of Code. If the Clash of Code hasn't started
            yet, this is the expected start time of the Clash of Code.

        end_time: Optional :class:`~datetime.datetime`
            End time of the Clash of Code.

        time_before_start: :class:`~datetime.timedelta`
            Time before the start of the Clash of Code.

        time_before_end: Optional :class:`~datetime.timedelta`
            Time before the end of the Clash of Code.

        players: :class:`list` of :class:`Player`
            List of the players in the Clash of Code.
    """

    public_handle: str
    join_url: str
    public: bool
    min_players: int
    max_players: int
    modes: Optional[Modes]
    programming_languages: Optional[LanguageIds]
    started: bool
    finished: bool
    mode: Optional[Mode]
    creation_time: Optional[datetime]
    start_time: datetime
    end_time: Optional[datetime]
    time_before_start: timedelta
    time_before_end: Optional[timedelta]
    players: List["Player"]

    __slots__ = (
        "public_handle",
        "join_url",
        "public",
        "min_players",
        "max_players",
        "modes",
        "programming_languages",
        "started",
        "finished",
        "mode",
        "creation_time",
        "start_time",
        "end_time",
        "time_before_start",
        "time_before_end",
        "players",
        "_test_session_handle",
        "_question",
    )

    def __init__(self, state: "ConnectionState", data: ClashOfCodeDict):
        self._test_session_handle: str = None
        self._question: Question = None
        super().__init__(state)
        self._set_data(data)

    def _set_data(self, data: ClashOfCodeDict):
        self._setattr("public_handle", data["publicHandle"])
        self._setattr(
            "join_url",
            f"https://www.codingame.com/clashofcode/clash/{self.public_handle}",
        )

        self._setattr("public", data.get("type", "PUBLIC") == "PUBLIC")
        self._setattr("min_players", data["nbPlayersMin"])
        self._setattr("max_players", data["nbPlayersMax"])
        self._setattr("modes", data.get("modes"))
        self._setattr("programming_languages", data.get("programmingLanguages"))

        self._setattr("started", data["started"])
        self._setattr("finished", data["finished"])
        self._setattr("mode", data.get("mode"))

        self._setattr("creation_time", to_datetime(data.get("creationTime")))
        self._setattr("start_time", to_datetime(data.get("startTimestamp")))
        self._setattr("end_time", to_datetime(data.get("endTime")))

        self._setattr(
            "time_before_start", timedelta(milliseconds=data["msBeforeStart"])
        )
        self._setattr(
            "time_before_end",
            (
                timedelta(milliseconds=data["msBeforeEnd"])
                if "msBeforeEnd" in data
                else None
            ),
        )

        self._setattr(
            "players",
            [
                Player(
                    self._state,
                    self,
                    self.started,
                    self.finished,
                    player,
                )
                for player in data.get("players", [])
            ]
            or minified_players_to_players(data.get("minifiedPlayers", [])),
        )

    def __repr__(self) -> str:
        return (
            "<ClashOfCode public_handle={0.public_handle!r} "
            "public={0.public!r} modes={0.modes!r} "
            "programming_languages={0.programming_languages!r} "
            "started={0.started!r} finished={0.finished!r} "
            "players={0.players!r}>".format(self)
        )

    def fetch(self):
        """|maybe_coro|

        Get and update the information about this Clash Of Code.

        This modifies this object's own attributes in place.
        """

        if self._state.is_async:

            async def _fetch():
                data = await self._state.http.get_clash_of_code_from_handle(
                    self.public_handle
                )
                self._set_data(data)

        else:

            def _fetch():
                data = self._state.http.get_clash_of_code_from_handle(
                    self.public_handle
                )
                self._set_data(data)

        return _fetch()

    def join(self, refetch: bool = False):
        """|maybe_coro|

        Join this Clash Of Code.

        You need to be logged in to join a Clash of Code or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            refetch: :class:`bool`
                Whether to update this object after joining.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _join():
                try:
                    await self._state.http.join_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    await self.fetch()

        else:

            def _join():
                try:
                    self._state.http.join_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    self.fetch()

        return _join()

    def start(self, refetch: bool = False):
        """|maybe_coro|

        Start this Clash Of Code.

        You need to be logged in as the owner to start a Clash of Code or else a
        :exc:`~codingame.LoginRequired` will be raised.

        .. note::
            This sets the countdown to the start to 5s. You will need to fetch
            the Clash Of Code again in 5-10s.

        Parameters
        -----------
            refetch: :class:`bool`
                Whether to update this object after starting.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _start():
                try:
                    await self._state.http.start_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    await self.fetch()

        else:

            def _start():
                try:
                    self._state.http.start_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    self.fetch()

        return _start()

    def leave(self, refetch: bool = False):
        """|maybe_coro|

        Leave this Clash Of Code.

        You need to be logged in or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            refetch: :class:`bool`
                Whether to update this object after leaving.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _leave():
                try:
                    await self._state.http.leave_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    await self.fetch()

        else:

            def _leave():
                try:
                    self._state.http.leave_clash_of_code_by_handle(
                        self._state.codingamer.id, self.public_handle
                    )
                except HTTPError as error:
                    if error.data["id"] in (504, 505, 506):
                        raise ClashOfCodeError.from_id(
                            error.data["id"], error.data.get("message")
                        )

                    raise  # pragma: no cover

                if refetch:
                    self.fetch()

        return _leave()

    def get_question(self, refetch: bool = False) -> "Question":
        """|maybe_coro|

        Get the question for this Clash of Code.

        You need to be logged in or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            refetch: :class:`bool`
                Whether to update this object after getting the question.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _get_question():
                if not self._question:
                    clash_test_session = (
                        await self._state.http.start_clash_test_session(
                            self._state.codingamer.id, self.public_handle
                        )
                    )
                    self._test_session_handle = clash_test_session["handle"]
                    test_session = (
                        await self._state.http.start_test_session_by_handle(
                            self._test_session_handle
                        )
                    )
                    self._question = Question(
                        self._state,
                        self,
                        test_session["currentQuestion"]["question"],
                    )

                if refetch:
                    await self.fetch()

                return self._question

        else:

            def _get_question():
                if not self._question:
                    clash_test_session = (
                        self._state.http.start_clash_test_session(
                            self._state.codingamer.id, self.public_handle
                        )
                    )
                    self._test_session_handle = clash_test_session["handle"]
                    test_session = (
                        self._state.http.start_test_session_by_handle(
                            self._test_session_handle
                        )
                    )
                    self._question = Question(
                        self._state,
                        self,
                        test_session["currentQuestion"]["question"],
                    )

                if refetch:
                    self.fetch()

                return self._question

        return _get_question()

    def play_test_cases(
        self,
        language_id: str,
        code: str,
        indexes: List[int] = None,
        refetch: bool = False,
    ) -> Dict[int, TestCaseResult]:
        """|maybe_coro|

        Play test cases for this Clash of Code with the given code.

        You need to be logged in or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            language_id: :class:`str`
                The language ID of the used programming language.
            code: :class:`str`
                The code to test against the test cases.
            indexes: :class:`list` of :class:`int`
                The indexes of the test cases to test the code.
                Default: all test cases
            refetch: :class:`bool`
                Whether to update this object after getting the question.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _play_test_cases():
                if not self._question:
                    await self.get_question()

                results = {}
                for test_case in self._question.test_cases:
                    if indexes and test_case.index not in indexes:
                        continue
                    result = await self._state.http.play_test_session_by_handle(
                        self._test_session_handle,
                        language_id,
                        code,
                        test_case.index,
                    )
                    results[test_case.index] = TestCaseResult(
                        self._state, self, test_case, result
                    )

                if refetch:
                    await self.fetch()

                return results

        else:

            def _play_test_cases():
                if not self._question:
                    self.get_question()

                results = {}
                for test_case in self._question.test_cases:
                    if indexes and test_case.index not in indexes:
                        continue
                    result = self._state.http.play_test_session_by_handle(
                        self._test_session_handle,
                        language_id,
                        code,
                        test_case.index,
                    )
                    results[test_case.index] = TestCaseResult(
                        self._state, self, test_case, result
                    )

                if refetch:
                    self.fetch()

                return results

        return _play_test_cases()

    def submit(
        self,
        language_id: str,
        code: str,
        refetch: bool = False,
    ) -> Solution:
        """|maybe_coro|

        Submit your solution for this Clash of .

        You need to be logged in or else a
        :exc:`~codingame.LoginRequired` will be raised.

        Parameters
        -----------
            language_id: :class:`str`
                The language ID of the used programming language.
            code: :class:`str`
                The code to test against the test cases.
            refetch: :class:`bool`
                Whether to update this object after getting the question.
                Default: `False`

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.
        """

        if not self._state.logged_in:
            raise LoginRequired()

        if self._state.is_async:

            async def _submit():
                if not self._question:
                    await self.get_question()

                solution_id = (
                    await self._state.http.submit_test_session_by_handle(
                        self._test_session_handle, language_id, code
                    )
                )
                solution = await self._state.http.get_solution_by_id(
                    self._state.codingamer.id, solution_id
                )

                if refetch:
                    await self.fetch()

                return Solution(self._state, self, solution)

        else:

            def _submit():
                if not self._question:
                    self.get_question()

                solution_id = self._state.http.submit_test_session_by_handle(
                    self._test_session_handle, language_id, code
                )
                solution = self._state.http.get_solution_by_id(
                    self._state.codingamer.id, solution_id
                )

                if refetch:
                    self.fetch()

                return Solution(self._state, self, solution)

        return _submit()
