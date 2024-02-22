from typing import TYPE_CHECKING, List

from ..abc import BaseObject
from ..codingamer import PartialCodinGamer
from ..types.clash_of_code import Contribution as ContributionDict
from ..types.clash_of_code import Question as QuestionDict
from ..types.clash_of_code import TestCase as TestCaseDict

if TYPE_CHECKING:
    from ..state import ConnectionState

__all__ = ("Contribution", "Question", "TestCase")


class TestCase(BaseObject):
    index: int
    input_binary_id: int
    output_binary_id: int

    def __init__(self, state: "ConnectionState", data: TestCaseDict):
        self.index = data["index"]
        self.input_binary_id = data["inputBinaryId"]
        self.output_binary_id = data["outputBinaryId"]

        super().__init__(state)


class Contribution(BaseObject):
    type: str
    status: str
    moderators: List[PartialCodinGamer]

    def __init__(self, state: "ConnectionState", data: ContributionDict):
        self.type = data["type"]
        self.status = data["status"]
        self.moderators = [
            PartialCodinGamer(state, mod) for mod in data["moderators"]
        ]

        super().__init__(state)


class Question(BaseObject):
    id: int
    initial_id: int
    type: str
    mode: str
    statement: str
    stub_generator: str
    duration: int
    index: int
    test_cases: List[TestCase]
    available_language_ids: str
    contributor: PartialCodinGamer
    contribution: Contribution

    def __init__(self, state: "ConnectionState", data: QuestionDict):
        self.id = data["id"]
        self.initial_id = data["initialId"]
        self.type = data["type"]
        self.mode = data["mode"]
        self.statement = data["statement"]
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
        self.contributor = PartialCodinGamer(state, data["contributor"])
        self.contribution = Contribution(state, data["contribution"])

        super().__init__(state)
