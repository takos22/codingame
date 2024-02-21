import datetime
import os

import pytest

from codingame import exceptions
from codingame.clash_of_code import ClashOfCode
from codingame.client import Client
from codingame.client.async_ import AsyncClient
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

pytestmark = pytest.mark.asyncio


async def test_client_create():
    client = Client(is_async=True)
    assert client.logged_in is False
    assert client.codingamer is None
    assert client.is_async is True


async def test_client_context_manager():
    async with Client(is_async=True) as client:
        assert client.logged_in is False
        assert client.codingamer is None
        assert client.is_async is True


async def test_client_context_manager_error():
    with pytest.raises(TypeError):
        with Client(is_async=True):
            pass  # pragma: no cover


async def test_client_request(client: AsyncClient):
    session = await client.request("session", "findSession")
    assert isinstance(session, dict)


@pytest.mark.parametrize(
    ["service", "func"],
    [
        ("", ""),
        ("session", ""),
        ("", "findSession"),
    ],
)
async def test_client_request_error(
    client: AsyncClient, service: str, func: str
):
    with pytest.raises(ValueError):
        await client.request(service, func)


async def test_client_login(client: AsyncClient, mock_http):
    mock_http(client._state.http, "login")
    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
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
async def test_client_login_error(
    client: AsyncClient,
    email: str,
    password: str,
):
    with pytest.raises(exceptions.LoginError):
        await client.login(email, password)


@pytest.mark.parametrize(
    "codingamer_query",
    [
        int(os.environ.get("TEST_CODINGAMER_ID")),
        os.environ.get("TEST_CODINGAMER_PSEUDO"),
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE"),
    ],
)
async def test_client_get_codingamer(
    client: AsyncClient, codingamer_query, mock_http
):
    mock_http(client._state.http, "search")
    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")

    codingamer = await client.get_codingamer(codingamer_query)
    assert isinstance(codingamer, CodinGamer)


@pytest.mark.parametrize(
    "codingamer_query",
    [
        0,
        "",
        "a" * 32 + "0" * 7,
    ],
)
async def test_client_get_codingamer_error(
    client: AsyncClient, codingamer_query, mock_http, mock_httperror
):
    mock_http(client._state.http, "search", [])
    mock_httperror(client._state.http, "get_codingamer_from_id", {"id": 404})
    mock_http(client._state.http, "get_codingamer_from_handle", None)

    with pytest.raises(exceptions.CodinGamerNotFound):
        await client.get_codingamer(codingamer_query)


async def test_client_get_clash_of_code(client: AsyncClient, mock_http):
    mock_http(client._state.http, "get_clash_of_code_from_handle")
    clash_of_code = await client.get_clash_of_code(
        os.environ.get("TEST_CLASHOFCODE_PUBLIC_HANDLE")
    )
    assert isinstance(clash_of_code, ClashOfCode)


async def test_client_get_clash_of_code_error(
    client: AsyncClient, mock_httperror
):
    with pytest.raises(ValueError):
        await client.get_clash_of_code("0")

    mock_httperror(
        client._state.http, "get_clash_of_code_from_handle", {"id": 502}
    )
    with pytest.raises(exceptions.ClashOfCodeNotFound):
        await client.get_clash_of_code("0" * 7 + "a" * 32)


async def test_client_get_pending_clash_of_code(client: AsyncClient, mock_http):
    mock_http(client._state.http, "get_pending_clash_of_code")
    clash_of_code = await client.get_pending_clash_of_code()
    assert isinstance(clash_of_code, ClashOfCode) or clash_of_code is None


async def test_client_create_private_clash_of_code(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "create_private_clash_of_code")
    mock_http(auth_client._state.http, "get_clash_of_code_from_handle")
    clash_of_code = await auth_client.create_private_clash_of_code(
        ["Python3"], ["SHORTEST", "FASTEST"]
    )
    assert isinstance(clash_of_code, ClashOfCode)
    assert clash_of_code.modes in (
        ["SHORTEST", "FASTEST"],
        ["FASTEST", "SHORTEST"],
    )
    assert clash_of_code.programming_languages == ["Python3"]
    assert auth_client.codingamer.id in [p.id for p in clash_of_code.players]


async def test_client_create_private_clash_of_code_logged_in_error(
    client: AsyncClient, mock_httperror
):
    with pytest.raises(exceptions.LoginRequired):
        await client.create_private_clash_of_code(
            ["Python3"], ["SHORTEST", "FASTEST"]
        )

    class C:
        def __init__(self):
            self.id = 0

    client._state.logged_in = True
    client._state.codingamer = C()

    mock_httperror(
        client._state.http,
        "create_private_clash_of_code",
        {"id": 501, "message": "You need to be logged to perform this action."},
    )
    with pytest.raises(exceptions.LoginRequired):
        await client.create_private_clash_of_code(
            ["Python3"], ["SHORTEST", "FASTEST"]
        )


async def test_client_create_private_clash_of_code_value_error(
    auth_client: AsyncClient,
):
    with pytest.raises(ValueError):
        await auth_client.create_private_clash_of_code(
            ["Python3"], ["BAD MODE", "FASTEST"]
        )


async def test_client_join_private_clash_of_code(
    auth_client: AsyncClient, private_clash: ClashOfCode, mock_http
):
    mock_http(auth_client._state.http, "join_clash_of_code_by_handle")
    mock_http(auth_client._state.http, "get_clash_of_code_from_handle")
    clash_of_code = await auth_client.join_private_clash_of_code(private_clash)
    assert isinstance(clash_of_code, ClashOfCode)
    assert private_clash.public_handle == clash_of_code.public_handle
    assert auth_client.codingamer.id in [p.id for p in clash_of_code.players]


async def test_client_join_private_clash_of_code_logged_in_error(
    client: AsyncClient,
):
    with pytest.raises(exceptions.LoginRequired):
        await client.join_private_clash_of_code("0" * 7 + "a" * 32)


async def test_client_join_private_clash_of_code_value_error(
    auth_client: AsyncClient, is_mocking: bool, mock_httperror
):
    with pytest.raises(ValueError):
        await auth_client.join_private_clash_of_code("not a public handle")

    mock_httperror(
        auth_client._state.http, "join_clash_of_code_by_handle", {"id": 502}
    )
    with pytest.raises(exceptions.ClashOfCodeNotFound):
        await auth_client.join_private_clash_of_code("0" * 7 + "a" * 32)

    if not is_mocking:
        return

    mock_httperror(
        auth_client._state.http, "join_clash_of_code_by_handle", {"id": 504}
    )
    with pytest.raises(exceptions.ClashOfCodeStarted):
        await auth_client.join_private_clash_of_code("0" * 7 + "a" * 32)

    mock_httperror(
        auth_client._state.http, "join_clash_of_code_by_handle", {"id": 505}
    )
    with pytest.raises(exceptions.ClashOfCodeFinished):
        await auth_client.join_private_clash_of_code("0" * 7 + "a" * 32)

    mock_httperror(
        auth_client._state.http, "join_clash_of_code_by_handle", {"id": 506}
    )
    with pytest.raises(exceptions.ClashOfCodeFull):
        await auth_client.join_private_clash_of_code("0" * 7 + "a" * 32)


async def test_client_get_language_ids(client: AsyncClient, mock_http):
    mock_http(client._state.http, "get_language_ids")
    language_ids = await client.get_language_ids()
    assert isinstance(language_ids, list)
    assert all(isinstance(language_id, str) for language_id in language_ids)


async def test_client_get_unseen_notifications(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "get_unseen_notifications")
    async for notification in auth_client.get_unseen_notifications():
        assert isinstance(notification, Notification)
        assert not notification.seen
        assert not notification.read


async def test_client_get_unseen_notifications_error(
    client: AsyncClient, is_mocking: bool, mock_http, mock_httperror
):
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_unseen_notifications():
            pass  # pragma: no cover

    if not is_mocking:
        return

    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
    )

    mock_httperror(client._state.http, "get_unseen_notifications", {"id": 492})
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_unseen_notifications():
            pass  # pragma: no cover


async def test_client_get_unread_notifications(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "get_unread_notifications")
    async for notification in auth_client.get_unread_notifications():
        assert isinstance(notification, Notification)
        assert not notification.read


async def test_client_get_unread_notifications_error(
    client: AsyncClient, is_mocking: bool, mock_http, mock_httperror
):
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_unread_notifications():
            pass  # pragma: no cover

    if not is_mocking:
        return

    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
    )

    mock_httperror(client._state.http, "get_unread_notifications", {"id": 492})
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_unread_notifications():
            pass  # pragma: no cover


async def test_client_get_read_notifications(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "get_last_read_notifications")
    async for notification in auth_client.get_read_notifications():
        assert isinstance(notification, Notification)
        assert notification.seen
        assert notification.read


async def test_client_get_read_notifications_error(
    client: AsyncClient, is_mocking: bool, mock_http, mock_httperror
):
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_read_notifications():
            pass  # pragma: no cover

    if not is_mocking:
        return

    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
    )

    mock_httperror(
        client._state.http, "get_last_read_notifications", {"id": 492}
    )
    with pytest.raises(exceptions.LoginRequired):
        async for _ in client.get_read_notifications():
            pass  # pragma: no cover


async def test_client_mark_notifications_as_seen(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "get_unseen_notifications")
    notifications = [n async for n in auth_client.get_unseen_notifications()]

    # if all notifications are seen, we dont want to fail the test
    if not notifications:  # pragma: no cover
        notifications = [
            n async for n in auth_client.get_unread_notifications()
        ]
    if not notifications:  # pragma: no cover
        notifications = [n async for n in auth_client.get_read_notifications()]

    notification: Notification = notifications[-1]

    mock_http(
        auth_client._state.http,
        "mark_notifications_as_seen",
        int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
    )
    seen_date = await auth_client.mark_notifications_as_seen(
        [notification, notification.id]
    )

    assert notification.seen
    assert notification.seen_date == seen_date
    assert notification.seen_date.timestamp() == pytest.approx(
        datetime.datetime.now(datetime.timezone.utc).timestamp(), abs=10_000
    )  # 10 seconds should be enough


async def test_client_mark_notifications_as_seen_error(
    client: AsyncClient, is_mocking: bool, mock_http, mock_httperror
):
    with pytest.raises(ValueError):
        await client.mark_notifications_as_seen([])

    with pytest.raises(exceptions.LoginRequired):
        await client.mark_notifications_as_seen([1])

    if not is_mocking:
        return

    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
    )

    mock_httperror(
        client._state.http, "mark_notifications_as_seen", {"id": 492}
    )
    with pytest.raises(exceptions.LoginRequired):
        await client.mark_notifications_as_seen([1])


async def test_client_mark_notifications_as_read(
    auth_client: AsyncClient, mock_http
):
    mock_http(auth_client._state.http, "get_unread_notifications")
    notifications = [n async for n in auth_client.get_unread_notifications()]

    # if all notifications are read, we dont want to fail the test
    if not notifications:  # pragma: no cover
        notifications = [n async for n in auth_client.get_read_notifications()]

    notification: Notification = notifications[-1]

    mock_http(
        auth_client._state.http,
        "mark_notifications_as_read",
        int(datetime.datetime.now().timestamp() * 1000),
    )
    read_date = await auth_client.mark_notifications_as_read(
        [notification, notification.id]
    )

    assert notification.read
    assert notification.read_date == read_date
    assert notification.read_date.timestamp() == pytest.approx(
        datetime.datetime.now().timestamp(), abs=10_000
    )  # 10 seconds should be enough


async def test_client_mark_notifications_as_read_error(
    client: AsyncClient, is_mocking: bool, mock_http, mock_httperror
):
    with pytest.raises(ValueError):
        await client.mark_notifications_as_read([])

    with pytest.raises(exceptions.LoginRequired):
        await client.mark_notifications_as_read([1])

    if not is_mocking:
        return

    mock_http(client._state.http, "get_codingamer_from_id")
    mock_http(client._state.http, "get_codingamer_from_handle")
    await client.login(
        remember_me_cookie=os.environ.get("TEST_LOGIN_REMEMBER_ME_COOKIE"),
    )

    mock_httperror(
        client._state.http, "mark_notifications_as_read", {"id": 492}
    )
    with pytest.raises(exceptions.LoginRequired):
        await client.mark_notifications_as_read([1])


async def test_client_get_global_leaderboard(client: AsyncClient):
    global_leaderboard = await client.get_global_leaderboard()
    assert isinstance(global_leaderboard, GlobalLeaderboard)
    assert isinstance(global_leaderboard.users[0], GlobalRankedCodinGamer)


async def test_client_get_global_leaderboard_error(client: AsyncClient):
    with pytest.raises(ValueError):
        await client.get_global_leaderboard(type="NONEXISTENT")
    with pytest.raises(ValueError):
        await client.get_global_leaderboard(group="nonexistent")
    with pytest.raises(exceptions.LoginRequired):
        await client.get_global_leaderboard(group="country")


@pytest.mark.parametrize(
    "challenge_id", ["coders-strike-back", "spring-challenge-2021"]
)
async def test_client_get_challenge_leaderboard(
    client: AsyncClient, challenge_id: str
):
    challenge_leaderboard = await client.get_challenge_leaderboard(challenge_id)
    assert isinstance(challenge_leaderboard, ChallengeLeaderboard)
    assert isinstance(challenge_leaderboard.users[0], ChallengeRankedCodinGamer)
    if challenge_leaderboard.has_leagues:
        assert isinstance(challenge_leaderboard.leagues[0], League)


async def test_client_get_challenge_leaderboard_error(client: AsyncClient):
    with pytest.raises(ValueError):
        await client.get_challenge_leaderboard(
            "spring-challenge-2021", group="nonexistent"
        )
    with pytest.raises(exceptions.LoginRequired):
        await client.get_challenge_leaderboard(
            "spring-challenge-2021", group="country"
        )
    with pytest.raises(exceptions.ChallengeNotFound):
        await client.get_challenge_leaderboard("nonexistent")


@pytest.mark.parametrize("puzzle_id", ["coders-strike-back", "codingame-optim"])
async def test_client_get_puzzle_leaderboard(
    client: AsyncClient, puzzle_id: str
):
    puzzle_leaderboard = await client.get_puzzle_leaderboard(puzzle_id)
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


async def test_client_get_puzzle_leaderboard_error(client: AsyncClient):
    with pytest.raises(ValueError):
        await client.get_puzzle_leaderboard(
            "codingame-optim", group="nonexistent"
        )
    with pytest.raises(exceptions.LoginRequired):
        await client.get_puzzle_leaderboard("codingame-optim", group="country")
    with pytest.raises(exceptions.PuzzleNotFound):
        await client.get_puzzle_leaderboard("nonexistent")
