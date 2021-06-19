import os
import pytest

from codingame.clash_of_code import ClashOfCode
from codingame.client import Client
from codingame.codingamer import CodinGamer
from codingame.exceptions import (
    ClashOfCodeNotFound,
    CodinGamerNotFound,
    LoginRequired,
)
from codingame.leaderboard import (
    ChallengeLeaderboard,
    ChallengeRankedCodinGamer,
    GlobalLeaderboard,
    GlobalRankedCodinGamer,
    League,
    PuzzleLeaderboard,
    PuzzleRankedCodinGamer,
)
from codingame.notification import Notification


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


def test_client_get_clash_of_code(client: Client):
    codingamer = client.get_clash_of_code(
        os.environ.get("TEST_CLASHOFCODE_PUBLIC_HANDLE")
    )
    assert isinstance(codingamer, ClashOfCode)


def test_client_get_clash_of_code_error(client: Client):
    with pytest.raises(ValueError):
        client.get_clash_of_code("0")

    with pytest.raises(ClashOfCodeNotFound):
        client.get_clash_of_code("0" * 7 + "a" * 32)


def test_client_language_ids(client: Client):
    language_ids = client.language_ids
    assert isinstance(language_ids, list)
    assert all(isinstance(language_id, str) for language_id in language_ids)

    # chaching
    assert hasattr(client, "_language_ids")
    language_ids = client.language_ids
    assert isinstance(language_ids, list)
    assert all(isinstance(language_id, str) for language_id in language_ids)


def test_client_notifications(auth_client: Client):
    for notification in auth_client.notifications:
        assert isinstance(notification, Notification)


def test_client_notifications_error(client: Client):
    with pytest.raises(LoginRequired):
        next(client.notifications)


def test_client_get_global_leaderboard(client: Client):
    global_leaderboard = client.get_global_leaderboard()
    assert isinstance(global_leaderboard, GlobalLeaderboard)
    assert isinstance(global_leaderboard.users[0], GlobalRankedCodinGamer)


def test_client_get_challenge_leaderboard(client: Client):
    challenge_leaderboard = client.get_challenge_leaderboard(
        "spring-challenge-2021"
    )
    assert isinstance(challenge_leaderboard, ChallengeLeaderboard)
    assert isinstance(challenge_leaderboard.users[0], ChallengeRankedCodinGamer)
    assert isinstance(challenge_leaderboard.leagues[0], League)


def test_client_get_puzzle_leaderboard(client: Client):
    puzzle_leaderboard = client.get_puzzle_leaderboard("codingame-optim")
    assert isinstance(puzzle_leaderboard, PuzzleLeaderboard)
    assert isinstance(puzzle_leaderboard.users[0], PuzzleRankedCodinGamer)
