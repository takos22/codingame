from typing import TYPE_CHECKING, List, Optional

from ..abc import BaseObject
from ..codingamer import PartialCodinGamer
from ..types.clash_of_code import Contribution as ContributionDict
from ..types.clash_of_code import Question as QuestionDict
from ..types.clash_of_code import TestCase as TestCaseDict

if TYPE_CHECKING:
    from ..state import ConnectionState
    from .clash_of_code import ClashOfCode

__all__ = ("Contribution", "Question", "TestCase", "TestCaseResult")


class TestCase(BaseObject):
    index: int
    label: Optional[str]
    input_binary_id: int
    output_binary_id: int

    def __init__(self, state: "ConnectionState", data: TestCaseDict):
        self.index = data["index"]
        self.label = data.get("label")
        self.input_binary_id = data["inputBinaryId"]
        self.output_binary_id = data["outputBinaryId"]

        super().__init__(state)


class TestCaseResult(BaseObject):
    """Represents the result of a test case run.

    Attributes
    -----------
        clash_of_code: :class:`ClashOfCode`
            The clash of code that is played.

        test_case: :class:`TestCase`
            The test case that has been played.

        success: :class:`bool`
            Whether the code succeeded with this test case.

        found: :class:`str`
            The output of the code.

        expected: :class:`str`
            The expected output for this test case.
    """

    clash_of_code: "ClashOfCode"
    test_case: TestCase
    success: bool
    found: str
    expected: str

    __slots__ = ("clash_of_code", "test_case", "success", "found", "expected")

    def __init__(
        self,
        state: "ConnectionState",
        clash_of_code: "ClashOfCode",
        test_case: TestCase,
        data: dict,
    ):
        self.clash_of_code = clash_of_code
        self.test_case = test_case
        self.success = data["comparison"]["success"]
        self.found = (
            data["comparison"]["found"]
            if "found" in data["comparison"]
            else data["output"]
        )
        self.expected = (
            data["output"] if self.success else data["comparison"]["expected"]
        )

        super().__init__(state)


class Contribution(BaseObject):
    type: str
    status: str
    contributor: Optional[PartialCodinGamer]
    moderators: List[PartialCodinGamer]

    def __init__(
        self,
        state: "ConnectionState",
        contributor: Optional[PartialCodinGamer],
        data: ContributionDict,
    ):
        self.type = data["type"]
        self.status = data["status"]
        self.contributor = contributor
        self.moderators = (
            [PartialCodinGamer(state, mod) for mod in data["moderators"]]
            if "moderators" in data
            else []
        )

        super().__init__(state)


class Question(BaseObject):
    clash_of_code: "ClashOfCode"
    id: int
    initial_id: int
    type: str
    mode: str
    raw_statement: str
    stub_generator: str
    duration: int
    index: int
    test_cases: List[TestCase]
    available_language_ids: str
    contribution: Optional[Contribution]

    def __init__(
        self,
        state: "ConnectionState",
        clash_of_code: "ClashOfCode",
        data: QuestionDict,
    ):
        self.clash_of_code = clash_of_code
        self.id = data["id"]
        self.initial_id = data["initialId"]
        self.type = data["type"]
        self.mode = data["mode"]
        self.raw_statement = data["statement"]
        self.stub_generator = data["stubGenerator"]
        self.duration = data["duration"]
        self.index = data["index"]
        self.test_cases = sorted(
            [TestCase(state, case) for case in data["testCases"]],
            key=lambda t: t.index,
        )
        self.available_language_ids = [
            lang["id"] for lang in data["availableLanguages"]
        ]
        contributor = (
            PartialCodinGamer(state, data["contributor"])
            if "contributor" in data
            else None
        )
        self.contribution = (
            Contribution(state, contributor, data["contribution"])
            if "contribution" in data
            else None
        )

        super().__init__(state)
