import json
import pytest
import typing

from pytest_mock import MockerFixture

if typing.TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser

    from codingame.http import HTTPClient


def pytest_addoption(parser: "Parser"):
    parser.addoption(
        "--no-mocking",
        action="store_true",
        default=False,
        help="Run tests with API calls",
    )


class FakeMocker:
    def __init__(self, *_, **__):
        pass

    def __getattr__(self, _):
        return FakeMocker()

    def __call__(self, *_, **__):
        pass


@pytest.fixture(name="mocker")
def mocker_fixture(pytestconfig: "Config"):
    mocker = (
        FakeMocker
        if pytestconfig.getoption("--no-mocking", default=True)
        else MockerFixture
    )

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
