import os

import pytest
from dotenv import load_dotenv

from codingame import Client

load_dotenv()


@pytest.fixture(name="client", scope="function")
def create_client() -> Client:
    with Client() as client:
        yield client


@pytest.fixture(name="auth_client")
def create_logged_in_client(request: pytest.FixtureRequest) -> Client:
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
