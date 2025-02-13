from typing import TYPE_CHECKING, List, Optional

from ..abc import BaseObject
from ..codingamer import PartialCodinGamer
from ..types.clash_of_code import Contribution as ContributionDict
from ..types.clash_of_code import Question as QuestionDict
from ..types.clash_of_code import TestCase as TestCaseDict

if TYPE_CHECKING:
    from ..state import ConnectionState
    from .clash_of_code import ClashOfCode

__all__ = ("ClashOfCodeContribution", "Question", "TestCase", "TestCaseResult")


class TestCase(BaseObject):
    index: int
    label: Optional[str]
    input_binary_id: int
    output_binary_id: int

    def __init__(self, state: "ConnectionState", data: TestCaseDict):
        self.index = data.get("index")
        self.label = data.get("label")
        self.input_binary_id = data.get("inputBinaryId")
        self.output_binary_id = data.get("outputBinaryId")

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
        comparison = data.get("comparison", {})
        self.success = comparison.get("success")
        self.found = comparison.get("found", data.get("output"))
        self.expected = (
            data.get("output") if self.success else comparison.get("expected")
        )

        super().__init__(state)


class ClashOfCodeContribution(BaseObject):
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
        self.type = data.get("type")
        self.status = data.get("status")
        self.contributor = contributor
        self.moderators = [
            PartialCodinGamer(state, mod) for mod in data.get("moderators", [])
        ]

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
    contribution: Optional[ClashOfCodeContribution]

    def __init__(
        self,
        state: "ConnectionState",
        clash_of_code: "ClashOfCode",
        data: QuestionDict,
    ):
        self.clash_of_code = clash_of_code
        self.id = data["id"]
        self.initial_id = data.get("initialId")
        self.type = data.get("type")
        self.mode = data.get("mode")
        self.raw_statement = data.get("statement")
        self.stub_generator = data.get("stubGenerator")
        self.duration = data.get("duration")
        self.index = data.get("index")
        self.test_cases = sorted(
            [TestCase(state, case) for case in data.get("testCases", [])],
            key=lambda t: t.index,
        )
        self.available_language_ids = [
            lang["id"] for lang in data.get("availableLanguages", [])
        ]
        contributor = (
            PartialCodinGamer(state, data["contributor"])
            if "contributor" in data
            else None
        )
        self.contribution = (
            ClashOfCodeContribution(state, contributor, data["contribution"])
            if "contribution" in data
            else None
        )

        super().__init__(state)
