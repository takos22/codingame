import os

import pytest

from codingame.client import Client
from codingame.codingamer import CodinGamer
from codingame.exceptions import LoginRequired


@pytest.fixture(name="codingamer")
def get_codingamer(auth_client, mock_http) -> CodinGamer:
    mock_http(auth_client._state.http, "get_codingamer_from_handle")
    return auth_client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )


def test_codingamer_avatar_and_cover_urls(client: Client, mock_http):
    mock_http(client._state.http, "get_codingamer_from_handle")
    codingamer = client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    assert isinstance(codingamer.avatar_url, str)
    assert isinstance(codingamer.cover_url, str)
    assert isinstance(codingamer.profile_url, str)


def test_codingamer_eq(client: Client, codingamer: CodinGamer, mock_http):
    mock_http(client._state.http, "get_codingamer_from_handle")
    other_codingamer = client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    assert codingamer == other_codingamer


def test_codingamer_get_followers(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_followers")
    for follower in codingamer.get_followers():
        assert isinstance(follower, CodinGamer)


def test_codingamer_get_followers_error(client: Client):
    codingamer = client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    with pytest.raises(LoginRequired):
        next(codingamer.get_followers())


def test_codingamer_get_followers_ids(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_follower_ids")
    followers_ids = codingamer.get_followers_ids()
    assert isinstance(followers_ids, list)
    assert all(isinstance(follower_id, int) for follower_id in followers_ids)


def test_codingamer_get_followed(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_following")
    for followed in codingamer.get_followed():
        assert isinstance(followed, CodinGamer)


def test_codingamer_get_followed_error(client: Client):
    codingamer = client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    with pytest.raises(LoginRequired):
        next(codingamer.get_followed())


def test_codingamer_get_followed_ids(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_following_ids")
    followed_ids = codingamer.get_followed_ids()
    assert isinstance(followed_ids, list)
    assert all(isinstance(followed_id, int) for followed_id in followed_ids)


def test_codingamer_get_clash_of_code_rank(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_clash_of_code_rank")
    rank = codingamer.get_clash_of_code_rank()
    assert isinstance(rank, int)
