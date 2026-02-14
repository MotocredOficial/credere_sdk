"""Shared test fixtures."""

import pytest

from credere.client import AsyncCredereClient, CredereClient

TEST_API_KEY = "sk-test-key"
TEST_BASE_URL = "https://api.credere.com"
TEST_STORE_ID = 42


@pytest.fixture
def sync_client() -> CredereClient:
    client = CredereClient(
        api_key=TEST_API_KEY, base_url=TEST_BASE_URL, store_id=TEST_STORE_ID
    )
    yield client  # type: ignore[misc]
    client.close()


@pytest.fixture
async def async_client() -> AsyncCredereClient:
    client = AsyncCredereClient(
        api_key=TEST_API_KEY, base_url=TEST_BASE_URL, store_id=TEST_STORE_ID
    )
    yield client  # type: ignore[misc]
    await client.close()
