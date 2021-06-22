import os
import pytest

import dotenv

from codingame import Client, CodinGamer

dotenv.load_dotenv()


@pytest.fixture(name="client", scope="function")
def create_client() -> Client:
    return Client()


@pytest.fixture(name="auth_client")
def create_logged_in_client() -> Client:
    client = Client()
    client.login(
        os.environ.get("TEST_LOGIN_EMAIL"),
        os.environ.get("TEST_LOGIN_PASSWORD"),
    )
    return client


@pytest.fixture(name="codingamer")
def get_codingamer(auth_client) -> CodinGamer:
    return auth_client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
