# TODO add more tests
import os
import re
import sys

import pytest
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath("..."))

from codingame.exceptions import ClashOfCodeNotFound


def test_import():
    import codingame

    assert (
        codingame.__title__
        == codingame.__name__
        == codingame.__package__
        == "codingame"
    )
    assert codingame.__author__ == "takos22"


@pytest.fixture
def codingame():
    import codingame

    return codingame


def client_attr(client):
    assert hasattr(client, "logged_in")
    assert hasattr(client, "codingamer")
    assert hasattr(client, "get_clash_of_code")
    assert hasattr(client, "get_pending_clash_of_code")
    assert hasattr(client, "get_codingamer")
    assert hasattr(client, "language_ids")
    assert hasattr(client, "notifications")
    return True


def test_client(codingame):
    client = codingame.Client()
    assert client_attr(client)


def test_client_login(codingame):
    email = os.environ.get("TEST_LOGIN_EMAIL")
    password = os.environ.get("TEST_LOGIN_PASSWORD")

    # login at creation
    client = codingame.Client(email, password)
    assert client_attr(client)

    # login after creation
    client = codingame.Client()
    client.login(email, password)
    assert client_attr(client)


@pytest.fixture
def client():
    import codingame

    return codingame.Client()


def test_client_codingamer_handle(codingame, client):
    codingamer = client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )

    assert type(codingamer) == codingame.CodinGamer


def test_client_codingamer_username(codingame, client):
    codingamer = client.get_codingamer("takos")

    assert type(codingamer) == codingame.CodinGamer


# TODO fix this
# @pytest.mark.parametrize("codingamer, error, message_regex", [
#     (0, TypeError, re.escape("Argument 'codingamer_' needs to be of type 'str' (got type 'int')")),
#     ("", ValueError, re.escape("CodinGamer handle '' isn't in the good format (regex: [0-9a-f]{32}[0-9]{7}).")),
#     ("a" * 32 + "0" * 7, CodinGamerNotFound, re.escape(f"No CodinGamer with public handle or username {'a' * 32 + '0' * 7!r}"))
# ])
# def test_client_codingamer_error(codingame, client, codingamer, error, message_regex):
#     with pytest.raises(error, match=message_regex):
#         codingamer = client.get_codingamer(codingamer)


def test_client_clash_of_code(codingame, client):
    clash_of_code = client.get_clash_of_code(
        os.environ.get("TEST_CLASHOFCODE_PUBLIC_HANDLE")
    )

    assert type(clash_of_code) == codingame.ClashOfCode


@pytest.mark.parametrize(
    "public_handle, error, message_regex",
    [
        (
            0,
            TypeError,
            re.escape(
                "Argument 'clash_of_code_handle' needs to be of type 'str' (got type 'int')"
            ),
        ),
        (
            "",
            ValueError,
            re.escape(
                "Clash of Code handle '' isn't in the good format (regex: [0-9]{7}[0-9a-f]{32})."
            ),
        ),
        (
            "0" * 7 + "a" * 32,
            ClashOfCodeNotFound,
            re.escape(f"No Clash of Code with handle {'0' * 7 + 'a' * 32!r}"),
        ),
    ],
)
def test_client_clash_of_code_error(
    codingame, client, public_handle, error, message_regex
):
    with pytest.raises(error, match=message_regex):
        client.get_clash_of_code(public_handle)


def test_client_pending_clash_of_code(codingame, client):
    clash_of_code = client.get_pending_clash_of_code()

    assert type(clash_of_code) == codingame.ClashOfCode or clash_of_code is None
