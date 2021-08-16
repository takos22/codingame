import os
import pytest

from codingame import exceptions
from codingame.clash_of_code import ClashOfCode
from codingame.client import Client
from codingame.codingamer import CodinGamer
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
    assert client.is_async is False


def test_client_context_manager():
    with Client() as client:
        assert client.logged_in is False
        assert client.codingamer is None
        assert client.is_async is False


@pytest.mark.asyncio
async def test_client_context_manager_error():
    with pytest.raises(TypeError):
        async with Client():
            pass  # pragma: no cover


def test_client_login(client: Client, mock_http):
    mock_http(client._state.http, "login")
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
        ("", "BadPassword"),
        ("NotAnEmail", ""),
        ("nonexistant@example.com", ""),
        ("nonexistant@example.com", "NonExistant"),
        (os.environ.get("TEST_LOGIN_EMAIL"), "BadPassword"),
    ],
)
def test_client_login_error(
    client: Client,
    email: str,
    password: str,
    is_mocking: bool,
    mock_httperror,
):
    if is_mocking:
        if email == "":
            error = {"id": 332, "message": "Email is required"}

        elif email == "NotAnEmail":
            error = {"id": 334, "message": "Malformed email"}

        elif email == "nonexistant@example.com":
            if password == "":
                error = {"id": 336, "message": "Password is required"}

            elif password == "NonExistant":
                error = {
                    "id": 393,
                    "message": (
                        "This email address is not linked to a "
                        "CodinGamer account"
                    ),
                }

        elif email == os.environ.get("TEST_LOGIN_EMAIL"):
            error = {
                "id": 396,
                "message": "The password you entered is incorrect.",
            }

        mock_httperror(client._state.http, "login", error)

    with pytest.raises(exceptions.LoginError):
        client.login(email, password)


@pytest.mark.parametrize(
    "codingamer_query",
    [
        int(os.environ.get("TEST_CODINGAMER_ID")),
        os.environ.get("TEST_CODINGAMER_PSEUDO"),
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE"),
    ],
)
def test_client_get_codingamer(client: Client, codingamer_query, mock_http):
    mock_http(client._state.http, "search")
    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")

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
def test_client_get_codingamer_error(
    client: Client, codingamer_query, mock_http, mock_httperror
):
    mock_http(client._state.http, "search", [])
    mock_httperror(client._state.http, "get_codingamer_from_id", {"id": 404})
    mock_http(client._state.http, "get_codingamer_from_handle", None)

    with pytest.raises(exceptions.CodinGamerNotFound):
        client.get_codingamer(codingamer_query)


def test_client_get_clash_of_code(client: Client):
    clash_of_code = client.get_clash_of_code(
        os.environ.get("TEST_CLASHOFCODE_PUBLIC_HANDLE")
    )
    assert isinstance(clash_of_code, ClashOfCode)


def test_client_get_clash_of_code_error(client: Client):
    with pytest.raises(ValueError):
        client.get_clash_of_code("0")

    with pytest.raises(exceptions.ClashOfCodeNotFound):
        client.get_clash_of_code("0" * 7 + "a" * 32)


def test_client_get_pending_clash_of_code(client: Client):
    clash_of_code = client.get_pending_clash_of_code()
    assert isinstance(clash_of_code, ClashOfCode) or clash_of_code is None


def test_client_get_language_ids(client: Client, mock_http):
    mock_http(client._state.http, "get_language_ids")
    language_ids = client.get_language_ids()
    assert isinstance(language_ids, list)
    assert all(isinstance(language_id, str) for language_id in language_ids)


def test_client_get_unseen_notifications(auth_client: Client):
    for notification in auth_client.get_unseen_notifications():
        assert isinstance(notification, Notification)
        assert not notification.seen
        assert not notification.read


def test_client_get_unseen_notifications_error(client: Client):
    with pytest.raises(exceptions.LoginRequired):
        next(client.get_unseen_notifications())


def test_client_get_unread_notifications(auth_client: Client):
    for notification in auth_client.get_unread_notifications():
        assert isinstance(notification, Notification)
        assert not notification.read


def test_client_get_unread_notifications_error(client: Client):
    with pytest.raises(exceptions.LoginRequired):
        next(client.get_unread_notifications())


def test_client_get_read_notifications(auth_client: Client):
    for notification in auth_client.get_read_notifications():
        assert isinstance(notification, Notification)
        assert notification.seen
        assert notification.read


def test_client_get_read_notifications_error(client: Client):
    with pytest.raises(exceptions.LoginRequired):
        next(client.get_read_notifications())


def test_client_get_global_leaderboard(client: Client):
    global_leaderboard = client.get_global_leaderboard()
    assert isinstance(global_leaderboard, GlobalLeaderboard)
    assert isinstance(global_leaderboard.users[0], GlobalRankedCodinGamer)


def test_client_get_global_leaderboard_error(client: Client):
    with pytest.raises(ValueError):
        client.get_global_leaderboard(type="NONEXISTENT")
    with pytest.raises(ValueError):
        client.get_global_leaderboard(group="nonexistent")
    with pytest.raises(exceptions.LoginRequired):
        client.get_global_leaderboard(group="country")


@pytest.mark.parametrize(
    "challenge_id", ["coders-strike-back", "spring-challenge-2021"]
)
def test_client_get_challenge_leaderboard(client: Client, challenge_id: str):
    challenge_leaderboard = client.get_challenge_leaderboard(challenge_id)
    assert isinstance(challenge_leaderboard, ChallengeLeaderboard)
    assert isinstance(challenge_leaderboard.users[0], ChallengeRankedCodinGamer)
    if challenge_leaderboard.has_leagues:
        assert isinstance(challenge_leaderboard.leagues[0], League)


def test_client_get_challenge_leaderboard_error(client: Client):
    with pytest.raises(ValueError):
        client.get_challenge_leaderboard(
            "spring-challenge-2021", group="nonexistent"
        )
    with pytest.raises(exceptions.LoginRequired):
        client.get_challenge_leaderboard(
            "spring-challenge-2021", group="country"
        )
    with pytest.raises(exceptions.ChallengeNotFound):
        client.get_challenge_leaderboard("nonexistent")


@pytest.mark.parametrize("puzzle_id", ["coders-strike-back", "codingame-optim"])
def test_client_get_puzzle_leaderboard(client: Client, puzzle_id: str):
    puzzle_leaderboard = client.get_puzzle_leaderboard(puzzle_id)
    assert isinstance(puzzle_leaderboard, PuzzleLeaderboard)
    assert isinstance(puzzle_leaderboard.users[0], PuzzleRankedCodinGamer)
    if puzzle_leaderboard.has_leagues:
        assert isinstance(puzzle_leaderboard.leagues[0], League)

        # test League.__eq__
        assert puzzle_leaderboard.leagues[0] == League(
            client._state,
            {
                "divisionCount": 6,
                "divisionIndex": 0,
                "divisionAgentsCount": 100,
            },
        )


def test_client_get_puzzle_leaderboard_error(client: Client):
    with pytest.raises(ValueError):
        client.get_puzzle_leaderboard("codingame-optim", group="nonexistent")
    with pytest.raises(exceptions.LoginRequired):
        client.get_puzzle_leaderboard("codingame-optim", group="country")
    with pytest.raises(exceptions.PuzzleNotFound):
        client.get_puzzle_leaderboard("nonexistent")
