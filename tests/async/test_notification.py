import datetime

import pytest

from codingame.client.async_ import AsyncClient
from codingame.notification import Notification

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="notification")
async def get_notification(auth_client: AsyncClient, mock_http) -> Notification:
    mock_http(auth_client._state.http, "get_unseen_notifications")
    notifications = [n async for n in auth_client.get_unseen_notifications()]

    # if all notifications are seen, we dont want to fail the test
    if not notifications:  # pragma: no cover
        notifications = [
            n async for n in auth_client.get_unread_notifications()
        ]
    if not notifications:  # pragma: no cover
        notifications = [
            n async for n in auth_client.get_last_read_notifications()
        ]

    return notifications[-1]


async def test_client_notification_mark_as_seen(
    auth_client: AsyncClient, notification: Notification, mock_http
):
    mock_http(
        auth_client._state.http,
        "mark_notifications_as_seen",
        int(datetime.datetime.utcnow().timestamp() * 1000),
    )
    seen_date = await notification.mark_as_seen()

    assert notification.seen
    assert notification.seen_date == seen_date
    assert notification.seen_date.timestamp() == pytest.approx(
        datetime.datetime.utcnow().timestamp(), abs=10_000
    )  # 10 seconds should be enough


async def test_client_notification_mark_as_read(
    auth_client: AsyncClient, notification: Notification, mock_http
):
    mock_http(
        auth_client._state.http,
        "mark_notifications_as_read",
        int(datetime.datetime.utcnow().timestamp() * 1000),
    )
    read_date = await notification.mark_as_read()

    assert notification.read
    assert notification.read_date == read_date
    assert notification.read_date.timestamp() == pytest.approx(
        datetime.datetime.utcnow().timestamp(), abs=10_000
    )  # 10 seconds should be enough
