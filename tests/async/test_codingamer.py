import os

import pytest

from codingame.client.async_ import AsyncClient
from codingame.codingamer import CodinGamer
from codingame.exceptions import LoginRequired

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="codingamer")
async def get_codingamer(auth_client, mock_http) -> CodinGamer:
    mock_http(auth_client._state.http, "get_codingamer_from_handle")
    return await auth_client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )


async def test_codingamer_avatar_and_cover_urls(client: AsyncClient, mock_http):
    mock_http(client._state.http, "get_codingamer_from_handle")
    codingamer = await client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    assert isinstance(codingamer.avatar_url, str)
    assert isinstance(codingamer.cover_url, str)
    assert isinstance(codingamer.profile_url, str)


async def test_codingamer_eq(
    client: AsyncClient, codingamer: CodinGamer, mock_http
):
    mock_http(client._state.http, "get_codingamer_from_handle")
    other_codingamer = await client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    assert codingamer == other_codingamer


async def test_codingamer_get_followers(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_followers")
    async for follower in codingamer.get_followers():
        assert isinstance(follower, CodinGamer)


async def test_codingamer_get_followers_error(client: AsyncClient):
    codingamer = await client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    with pytest.raises(LoginRequired):
        next(await codingamer.get_followers())


async def test_codingamer_get_followers_ids(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_follower_ids")
    followers_ids = await codingamer.get_followers_ids()
    assert isinstance(followers_ids, list)
    assert all(isinstance(follower_id, int) for follower_id in followers_ids)


async def test_codingamer_get_followed(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_following")
    async for followed in codingamer.get_followed():
        assert isinstance(followed, CodinGamer)


async def test_codingamer_get_followed_error(client: AsyncClient):
    codingamer = await client.get_codingamer(
        os.environ.get("TEST_CODINGAMER_PUBLIC_HANDLE")
    )
    with pytest.raises(LoginRequired):
        next(await codingamer.get_followed())


async def test_codingamer_get_followed_ids(codingamer: CodinGamer, mock_http):
    mock_http(codingamer._state.http, "get_codingamer_following_ids")
    followed_ids = await codingamer.get_followed_ids()
    assert isinstance(followed_ids, list)
    assert all(isinstance(followed_id, int) for followed_id in followed_ids)


async def test_codingamer_get_clash_of_code_rank(
    codingamer: CodinGamer, mock_http
):
    mock_http(codingamer._state.http, "get_codingamer_clash_of_code_rank")
    rank = await codingamer.get_clash_of_code_rank()
    assert isinstance(rank, int)
