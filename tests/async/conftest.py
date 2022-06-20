import os

import pytest
from dotenv import load_dotenv

from codingame import Client
from codingame.client.async_ import AsyncClient

load_dotenv()


@pytest.fixture(name="client", scope="function")
async def create_client() -> AsyncClient:
    async with Client(is_async=True) as client:
        yield client


@pytest.fixture(name="auth_client")
async def create_logged_in_client(
    request: pytest.FixtureRequest,
) -> AsyncClient:
    async with Client(is_async=True) as client:
        if "mock_http" in request.fixturenames:
            mock_http = request.getfixturevalue("mock_http")
            mock_http(client._state.http, "login")
            mock_http(client._state.http, "get_codingamer_from_id")
            mock_http(client._state.http, "get_codingamer_from_handle")

        await client.login(
            remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
        )
        yield client
