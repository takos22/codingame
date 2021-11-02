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
def create_logged_in_client() -> Client:
    with Client() as client:
        client.login(
            remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
        )
        yield client
