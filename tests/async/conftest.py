import os
import pytest

import dotenv

from codingame import Client
from codingame.client.async_ import AsyncClient

dotenv.load_dotenv()


@pytest.fixture(name="client", scope="function")
async def create_client() -> AsyncClient:
    async with Client(is_async=True) as client:
        yield client


@pytest.fixture(name="auth_client")
async def create_logged_in_client() -> AsyncClient:
    async with Client(is_async=True) as client:
        await client.login(
            os.environ.get("TEST_LOGIN_EMAIL"),
            os.environ.get("TEST_LOGIN_PASSWORD"),
        )
        yield client
