import os
import pytest

from codingame.client import Client
from codingame.codingamer import CodinGamer
from codingame.exceptions import CodinGamerNotFound


def test_client_create():
    client = Client()
    assert client.logged_in is False
    assert client.codingamer is None


def test_client_create_with_login():
    client = Client(
        os.environ.get("TEST_LOGIN_EMAIL"),
        os.environ.get("TEST_LOGIN_PASSWORD"),
    )
    assert client.logged_in is True
    assert client.codingamer is not None


def test_client_login(client: Client):
    client.login(
        os.environ.get("TEST_LOGIN_EMAIL"),
        os.environ.get("TEST_LOGIN_PASSWORD"),
    )
    assert client.logged_in is True
    assert client.codingamer is not None


@pytest.mark.parametrize(
    ["email", "password"],
    [
        ("", ""),
        (os.environ.get("TEST_LOGIN_EMAIL"), ""),
        (os.environ.get("TEST_LOGIN_EMAIL"), "BadPassword"),
        ("nonexistant", "NonExistant"),
        ("nonexistant@example.com", "NonExistant"),
    ],
)
def test_client_login_error(client: Client, email: str, password: str):
    with pytest.raises(ValueError):
        client.login(email, password)


@pytest.mark.parametrize(
    "codingamer_query",
    [
        int(os.environ.get("TEST_CODINGAMER_ID")),
        os.environ.get("TEST_CODINGAMER_PSEUDO"),
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE"),
    ],
)
def test_client_get_codingamer(client: Client, codingamer_query):
    codingamer = client.get_codingamer(codingamer_query)
    assert isinstance(codingamer, CodinGamer)


@pytest.mark.parametrize(
    "codingamer_query",
    [
        0,
        "",
        "a" * 32 + "0" * 7,
    ],
)
def test_client_get_codingamer_error(client: Client, codingamer_query):
    with pytest.raises(CodinGamerNotFound):
        client.get_codingamer(codingamer_query)
