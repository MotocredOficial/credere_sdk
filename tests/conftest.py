"""Shared test fixtures."""

import pytest

from credere.client import AsyncCredereClient, CredereClient

TEST_API_KEY = "sk-test-key"
TEST_BASE_URL = "https://api.credere.com"


@pytest.fixture
def sync_client() -> CredereClient:
    client = CredereClient(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)
    yield client  # type: ignore[misc]
    client.close()


@pytest.fixture
async def async_client() -> AsyncCredereClient:
    client = AsyncCredereClient(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)
    yield client  # type: ignore[misc]
    await client.close()
