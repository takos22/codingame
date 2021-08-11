import json
import pytest
import typing

from pytest_mock import MockerFixture

from codingame.http import HTTPError

if typing.TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser

    from codingame.http import HTTPClient


def pytest_addoption(parser: "Parser"):
    parser.addoption(
        "--nm",
        "--no-mocking",
        action="store_true",
        dest="no_mocking",
        help="Run tests with API calls",
    )


@pytest.fixture(name="is_mocking")
def is_mocking_fixture(pytestconfig: "Config"):
    return not pytestconfig.getoption("no_mocking", default=False)


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


def awaitable(obj):
    async def f():
        return obj

    return f()


@pytest.fixture(name="mock_http")
def mock_http_fixture(mocker: MockerFixture):
    def mock_http(
        http_client: "HTTPClient", method: str, api_data=None, *args, **kwargs
    ):
        if api_data is None:
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
