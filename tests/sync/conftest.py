import os
import sys

import pytest
from dotenv import load_dotenv

from codingame import ClashOfCode, Client
from codingame.client.sync import SyncClient

load_dotenv()


@pytest.fixture(name="client", scope="function")
def create_client() -> SyncClient:
    with Client() as client:
        yield client


@pytest.fixture(name="auth_client")
def create_logged_in_client(mock_http) -> SyncClient:
    with Client() as client:
        mock_http(client._state.http, "login")
        mock_http(client._state.http, "get_codingamer_from_id")
        mock_http(client._state.http, "get_codingamer_from_handle")

        client.login(
            remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
        )
        yield client


@pytest.fixture(name="auth_client_bis")
def create_logged_in_client_bis(mock_http) -> SyncClient:
    with Client() as client:
        mock_http(client._state.http, "login")
        mock_http(client._state.http, "get_codingamer_from_id")
        mock_http(
            client._state.http,
            "get_codingamer_from_handle",
            api_data_filename="get_codingamer_from_handle.bis",
        )

        client.login(
            remember_me_cookie=os.environ.get(
                "TEST_LOGIN_REMEMBER_ME_COOKIE_{0.major}{0.minor}".format(
                    sys.version_info
                )
            ),
        )

        yield client


@pytest.fixture(name="private_clash")
def create_private_clash(auth_client: SyncClient, mock_http) -> ClashOfCode:
    mock_http(auth_client._state.http, "create_private_clash_of_code")
    mock_http(auth_client._state.http, "get_clash_of_code_from_handle")

    clash_of_code = auth_client.create_private_clash_of_code(
        ["Python3"], ["SHORTEST", "FASTEST"]
    )
    yield clash_of_code
