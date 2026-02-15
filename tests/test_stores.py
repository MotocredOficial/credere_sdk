"""Tests for the Stores resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.stores import Store, StoreCreateRequest

BASE_URL = "https://api.credere.com"
STORES_URL = f"{BASE_URL}/v1/stores"

SAMPLE_STORE_RESPONSE = {
    "store": {
        "id": 1,
        "name": "Test Store",
        "display_name": "Test",
        "cnpj": "12345678000100",
        "created_at": "2024-01-15T10:00:00-03:00",
        "updated_at": "2024-01-15T10:00:00-03:00",
    }
}

SAMPLE_LIST_RESPONSE = {"stores": [SAMPLE_STORE_RESPONSE["store"]]}

SAMPLE_CREATE_DATA = StoreCreateRequest(
    name="Test Store",
    display_name="Test",
    cnpj="12345678000100",
)


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestStoresCreate:
    @respx.mock
    def test_create_store(self, sync_client: CredereClient) -> None:
        route = respx.post(STORES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_STORE_RESPONSE)
        )

        result = sync_client.stores.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert result.name == "Test Store"
        assert result.display_name == "Test"
        assert result.cnpj == "12345678000100"


class TestStoresList:
    @respx.mock
    def test_list_stores(self, sync_client: CredereClient) -> None:
        route = respx.get(STORES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = sync_client.stores.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Store)
        assert result[0].name == "Test Store"


class TestStoresActivate:
    @respx.mock
    def test_activate_store(self, sync_client: CredereClient) -> None:
        url = f"{STORES_URL}/1/activate"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_STORE_RESPONSE)
        )

        result = sync_client.stores.activate(1)

        assert route.called
        assert isinstance(result, Store)
        assert result.name == "Test Store"


class TestStoresDeactivate:
    @respx.mock
    def test_deactivate_store(self, sync_client: CredereClient) -> None:
        url = f"{STORES_URL}/1/deactivate"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_STORE_RESPONSE)
        )

        result = sync_client.stores.deactivate(1)

        assert route.called
        assert isinstance(result, Store)
        assert result.name == "Test Store"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(STORES_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.stores.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{STORES_URL}/999/activate"
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
            sync_client.stores.activate(999)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncStoresCreate:
    @respx.mock
    async def test_async_create_store(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(STORES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_STORE_RESPONSE)
        )

        result = await async_client.stores.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert result.name == "Test Store"


class TestAsyncStoresList:
    @respx.mock
    async def test_async_list_stores(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(STORES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = await async_client.stores.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Store)
        assert result[0].name == "Test Store"
