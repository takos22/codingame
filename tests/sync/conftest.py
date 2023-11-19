import os

import pytest
from dotenv import load_dotenv

from codingame import Client, ClashOfCode
from codingame.client.sync import SyncClient

load_dotenv()


@pytest.fixture(name="client", scope="function")
def create_client() -> SyncClient:
    with Client() as client:
        yield client


@pytest.fixture(name="auth_client")
def create_logged_in_client(request: pytest.FixtureRequest) -> SyncClient:
    with Client() as client:
        if "mock_http" in request.fixturenames:
            mock_http = request.getfixturevalue("mock_http")
            mock_http(client._state.http, "login")
            mock_http(client._state.http, "get_codingamer_from_id")
            mock_http(client._state.http, "get_codingamer_from_handle")

        client.login(
            remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
        )
        yield client


@pytest.fixture(name="private_clash")
def create_private_clash(
    request: pytest.FixtureRequest, auth_client: SyncClient
) -> ClashOfCode:
    if "mock_http" in request.fixturenames:
        mock_http = request.getfixturevalue("mock_http")
        mock_http(auth_client._state.http, "create_private_clash_of_code")
        mock_http(auth_client._state.http, "get_clash_of_code_from_handle")

    clash_of_code = auth_client.create_private_clash_of_code(
        ["Python3"], ["SHORTEST", "FASTEST"]
    )
    yield clash_of_code
