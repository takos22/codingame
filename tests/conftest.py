import json
import os
import sys
import typing

import pytest
from dotenv import load_dotenv
from pytest_mock import MockerFixture

from codingame.http import HTTPError

if typing.TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser

    from codingame.http import HTTPClient

load_dotenv()


def mock_environ(force_new=True):
    set_environ = os.environ.__setitem__ if force_new else os.environ.setdefault

    set_environ("TEST_LOGIN_EMAIL", "email@example.com")
    set_environ("TEST_LOGIN_PASSWORD", "VerySafePassword")
    set_environ(
        "TEST_LOGIN_REMEMBER_ME_COOKIE",
        "1234567fedcba9876543210fedcba9876543210",
    )

    set_environ("TEST_CODINGAMER_ID", "1234567")
    set_environ("TEST_CODINGAMER_PSEUDO", "Pseudo123")
    set_environ(
        "TEST_CODINGAMER_PUBLIC_HANDLE",
        "0123456789abcdef0123456789abcdef7654321",
    )

    set_environ(
        "TEST_CLASHOFCODE_PUBLIC_HANDLE",
        "1234567fedcba9876543210fedcba9876543210",
    )


if all(opt not in sys.argv[1:] for opt in ("--nm", "--no-mocking")):
    mock_environ()


def pytest_addoption(parser: "Parser"):
    parser.addoption(
        "--nm",
        "--no-mocking",
        action="store_true",
        dest="no_mocking",
        help="Run all tests without mocking the API calls.",
    )
    parser.addoption(
        "--om",
        "--only-mocked",
        action="store_true",
        dest="only_mocked",
        help="Only run tests that have been mocked.",
    )


def pytest_collection_modifyitems(
    config: "Config", items: typing.List[pytest.Item]
):
    mocking_fixture_name = "mocker"
    if config.getoption("only_mocked", default=False):
        selected_items = []
        deselected_items = []

        for item in items:
            if mocking_fixture_name in getattr(item, "fixturenames", ()):
                selected_items.append(item)
            else:
                deselected_items.append(item)

        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items


@pytest.fixture(name="is_mocking", scope="session")
def is_mocking_fixture(pytestconfig: "Config"):
    return not pytestconfig.getoption("no_mocking", default=False)


@pytest.fixture(name="mock_environ", scope="session", autouse=True)
def mock_environ_fixture(is_mocking: bool):
    if is_mocking:
        mock_environ()


class FakeMocker:
    def __init__(self, *_, **__):
        pass

    def __getattr__(self, _):
        return FakeMocker()  # for attribute of attribute

    def __call__(self, *_, **__):
        pass


@pytest.fixture(name="mocker")
def mocker_fixture(is_mocking: bool, pytestconfig: "Config"):
    mocker = MockerFixture if is_mocking else FakeMocker

    # imitate https://github.com/pytest-dev/pytest-mock/blob/main/src/pytest_mock/plugin.py#L388 # noqa: E501
    result = mocker(pytestconfig)
    yield result
    result.stopall()


not_set = object()


def awaitable(obj):
    async def f():
        return obj

    return f()


@pytest.fixture(name="mock_http")
def mock_http_fixture(mocker: MockerFixture):
    def mock_http(
        http_client: "HTTPClient",
        method: str,
        api_data=not_set,
        *args,
        **kwargs,
    ):
        if api_data is not_set:
            with open(f"tests/mock/responses/{method}.json") as f:
                api_data = json.load(f)

        mocker.patch.object(
            http_client,
            method,
            new=lambda *_: (
                awaitable(api_data) if http_client.is_async else api_data
            ),
            *args,
            **kwargs,
        )

    return mock_http


@pytest.fixture(name="mock_httperror")
def mock_httperror_fixture(mocker: MockerFixture):
    def mock_httperror(
        http_client: "HTTPClient", method: str, api_data, *args, **kwargs
    ):
        error = HTTPError(422, "", api_data)
        if http_client.is_async:

            async def fake_api_call(*_):
                raise error

        else:

            def fake_api_call(*_):
                raise error

        mocker.patch.object(
            http_client, method, new=fake_api_call, *args, **kwargs
        )

    return mock_httperror
