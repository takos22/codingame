import datetime

import pytest

from codingame.client.sync import SyncClient
from codingame.notification import Notification


@pytest.fixture(name="notification")
def get_notification(auth_client: SyncClient, mock_http) -> Notification:
    mock_http(auth_client._state.http, "get_unseen_notifications")
    notifications = list(auth_client.get_unseen_notifications())

    # if all notifications are seen or read, we dont want to fail the test
    if not notifications:  # pragma: no cover
        notifications = list(auth_client.get_unread_notifications())
    if not notifications:  # pragma: no cover
        notifications = list(auth_client.get_last_read_notifications())

    return notifications[-1]


def test_client_notification_mark_as_seen(
    auth_client: SyncClient, notification: Notification, mock_http
):
    mock_http(
        auth_client._state.http,
        "mark_notifications_as_seen",
        int(datetime.datetime.utcnow().timestamp() * 1000),
    )
    seen_date = notification.mark_as_seen()

    assert notification.seen
    assert notification.seen_date == seen_date
    assert notification.seen_date.timestamp() == pytest.approx(
        datetime.datetime.utcnow().timestamp(), abs=10_000
    )  # 10 seconds should be enough


def test_client_notification_mark_as_read(
    auth_client: SyncClient, notification: Notification, mock_http
):
    mock_http(
        auth_client._state.http,
        "mark_notifications_as_read",
        int(datetime.datetime.utcnow().timestamp() * 1000),
    )
    read_date = notification.mark_as_read()

    assert notification.read
    assert notification.read_date == read_date
    assert notification.read_date.timestamp() == pytest.approx(
        datetime.datetime.utcnow().timestamp(), abs=10_000
    )  # 10 seconds should be enough
