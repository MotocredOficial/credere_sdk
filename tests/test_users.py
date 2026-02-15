"""Tests for the Users resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError
from credere.models.users import User

BASE_URL = "https://api.credere.com"
USERS_URL = f"{BASE_URL}/v1/users"

SAMPLE_USER = {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "cpf": "12345678901",
    "created_at": "2024-01-15T10:00:00-03:00",
    "updated_at": "2024-01-15T10:00:00-03:00",
}

SAMPLE_CURRENT_RESPONSE = {"user": SAMPLE_USER}
SAMPLE_PROPOSALS_FILTER_LIST_RESPONSE = {"users": [SAMPLE_USER]}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestUsersCurrent:
    @respx.mock
    def test_current_returns_user(self, sync_client: CredereClient) -> None:
        url = f"{USERS_URL}/current"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CURRENT_RESPONSE)
        )

        result = sync_client.users.current()

        assert route.called
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "John"
        assert result.email == "john@example.com"
        assert result.cpf == "12345678901"


class TestUsersProposalsFilterList:
    @respx.mock
    def test_proposals_filter_list_returns_list_of_users(
        self, sync_client: CredereClient
    ) -> None:
        url = f"{USERS_URL}/proposals_filter_list"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_FILTER_LIST_RESPONSE)
        )

        result = sync_client.users.proposals_filter_list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], User)
        assert result[0].name == "John"

    @respx.mock
    def test_proposals_filter_list_sends_store_id_header(
        self, sync_client: CredereClient
    ) -> None:
        url = f"{USERS_URL}/proposals_filter_list"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_FILTER_LIST_RESPONSE)
        )

        sync_client.users.proposals_filter_list()

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        url = f"{USERS_URL}/current"
        respx.get(url).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.users.current()

        assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncUsersCurrent:
    @respx.mock
    async def test_async_current_returns_user(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{USERS_URL}/current"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CURRENT_RESPONSE)
        )

        result = await async_client.users.current()

        assert route.called
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "John"
        assert result.email == "john@example.com"
        assert result.cpf == "12345678901"


class TestAsyncUsersProposalsFilterList:
    @respx.mock
    async def test_async_proposals_filter_list_returns_list_of_users(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{USERS_URL}/proposals_filter_list"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_FILTER_LIST_RESPONSE)
        )

        result = await async_client.users.proposals_filter_list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], User)
        assert result[0].name == "John"
