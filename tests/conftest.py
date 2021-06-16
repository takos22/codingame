import os
import pytest

import dotenv

from codingame.client import Client

dotenv.load_dotenv()


@pytest.fixture(name="client")
def create_client() -> Client:
    return Client()


@pytest.fixture(name="auth_client")
def create_logged_in_client(client) -> Client:
    client.login(
        os.environ.get("TEST_LOGIN_EMAIL"),
        os.environ.get("TEST_LOGIN_PASSWORD"),
    )
    return client
