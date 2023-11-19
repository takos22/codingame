import os

import pytest
from dotenv import load_dotenv

from codingame import ClashOfCode, Client
from codingame.client.async_ import AsyncClient

load_dotenv()


@pytest.fixture(name="client", scope="function")
async def create_client() -> AsyncClient:
    async with Client(is_async=True) as client:
        yield client


@pytest.fixture(name="auth_client")
async def create_logged_in_client(mock_http) -> AsyncClient:
    async with Client(is_async=True) as client:
        mock_http(client._state.http, "login")
        mock_http(client._state.http, "get_codingamer_from_id")
        mock_http(client._state.http, "get_codingamer_from_handle")

        await client.login(
            remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
        )
        yield client


@pytest.fixture(name="private_clash")
async def create_private_clash(
    auth_client: AsyncClient, mock_http
) -> ClashOfCode:
    mock_http(auth_client._state.http, "create_private_clash_of_code")
    mock_http(auth_client._state.http, "get_clash_of_code_from_handle")

    clash_of_code = await auth_client.create_private_clash_of_code(
        ["Python3"], ["SHORTEST", "FASTEST"]
    )
    yield clash_of_code
