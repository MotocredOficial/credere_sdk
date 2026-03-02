"""Shared test fixtures."""

import pytest

from credere.client import AsyncCredereClient, CredereClient

from .config import API_KEY, BASE_URL, STORE_ID


@pytest.fixture
def sync_client() -> CredereClient:
    client = CredereClient(api_key=API_KEY, base_url=BASE_URL, store_id=STORE_ID)
    yield client  # type: ignore[misc]
    client.close()


@pytest.fixture
async def async_client() -> AsyncCredereClient:
    client = AsyncCredereClient(api_key=API_KEY, base_url=BASE_URL, store_id=STORE_ID)
    yield client  # type: ignore[misc]
    await client.close()
