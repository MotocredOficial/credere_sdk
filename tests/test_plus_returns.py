"""Tests for the Plus Returns resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.plus_returns import PlusReturnRule, PlusReturnRuleCreateRequest

BASE_URL = "https://api.credere.com"
RULES_URL = f"{BASE_URL}/v1/plus_return_rules"

SAMPLE_RULE_RESPONSE = {
    "plus_return_rule": {
        "id": 1,
        "created_at": "2024-01-01",
        "updated_at": "2024-01-01",
    }
}

SAMPLE_LIST_RESPONSE = [SAMPLE_RULE_RESPONSE["plus_return_rule"]]

SAMPLE_CREATE_DATA = PlusReturnRuleCreateRequest()


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestPlusReturnsCreate:
    @respx.mock
    def test_create(self, sync_client: CredereClient) -> None:
        route = respx.post(RULES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = sync_client.plus_returns.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1
        assert result.created_at == "2024-01-01"
        assert result.updated_at == "2024-01-01"


class TestPlusReturnsList:
    @respx.mock
    def test_list(self, sync_client: CredereClient) -> None:
        route = respx.get(RULES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = sync_client.plus_returns.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], PlusReturnRule)
        assert result[0].id == 1


class TestPlusReturnsGet:
    @respx.mock
    def test_get(self, sync_client: CredereClient) -> None:
        url = f"{RULES_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = sync_client.plus_returns.get(1)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1
        assert result.created_at == "2024-01-01"


class TestPlusReturnsUpdate:
    @respx.mock
    def test_update(self, sync_client: CredereClient) -> None:
        url = f"{RULES_URL}/1"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = sync_client.plus_returns.update(1, SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1


class TestPlusReturnsDelete:
    @respx.mock
    def test_delete(self, sync_client: CredereClient) -> None:
        route = respx.delete(f"{RULES_URL}/1").mock(
            return_value=httpx.Response(200, json={})
        )

        result = sync_client.plus_returns.delete(1)

        assert route.called
        assert result is None


class TestPlusReturnsActivate:
    @respx.mock
    def test_activate(self, sync_client: CredereClient) -> None:
        url = f"{RULES_URL}/1/activate"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = sync_client.plus_returns.activate(1)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1


class TestPlusReturnsDeactivate:
    @respx.mock
    def test_deactivate(self, sync_client: CredereClient) -> None:
        url = f"{RULES_URL}/1/deactivate"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = sync_client.plus_returns.deactivate(1)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(RULES_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.plus_returns.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{RULES_URL}/999"
        respx.get(url).mock(
            return_value=httpx.Response(
                404,
                json={
                    "error": {
                        "message": "Endpoint requested not found",
                        "status": 404,
                    }
                },
            )
        )

        with pytest.raises(NotFoundError) as exc_info:
            sync_client.plus_returns.get(999)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncPlusReturnsCreate:
    @respx.mock
    async def test_async_create(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(RULES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = await async_client.plus_returns.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1
        assert result.created_at == "2024-01-01"


class TestAsyncPlusReturnsList:
    @respx.mock
    async def test_async_list(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(RULES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = await async_client.plus_returns.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], PlusReturnRule)


class TestAsyncPlusReturnsGet:
    @respx.mock
    async def test_async_get(self, async_client: AsyncCredereClient) -> None:
        url = f"{RULES_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_RULE_RESPONSE)
        )

        result = await async_client.plus_returns.get(1)

        assert route.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == 1


class TestAsyncPlusReturnsDelete:
    @respx.mock
    async def test_async_delete(self, async_client: AsyncCredereClient) -> None:
        route = respx.delete(f"{RULES_URL}/1").mock(
            return_value=httpx.Response(200, json={})
        )

        result = await async_client.plus_returns.delete(1)

        assert route.called
        assert result is None
