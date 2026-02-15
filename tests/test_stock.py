"""Tests for the Stock resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.stock import StockVehicle, StockVehicleCreateRequest

BASE_URL = "https://api.credere.com"
VEHICLES_URL = f"{BASE_URL}/v1/vehicles"

SAMPLE_VEHICLE = {
    "id": 1,
    "price_cents": 5000000,
    "description": "Test vehicle",
    "created_at": "2024-01-15T10:00:00-03:00",
    "updated_at": "2024-01-15T10:00:00-03:00",
}

SAMPLE_CREATE_DATA = StockVehicleCreateRequest(
    vehicle_model_id=10,
    store_id=42,
    price_cents=5000000,
    description="Test vehicle",
)


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestStockCreate:
    @respx.mock
    def test_create_returns_stock_vehicle(self, sync_client: CredereClient) -> None:
        route = respx.post(VEHICLES_URL).mock(
            return_value=httpx.Response(200, json={"vehicle": SAMPLE_VEHICLE})
        )

        vehicle = sync_client.stock.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(vehicle, StockVehicle)
        assert vehicle.id == 1
        assert vehicle.price_cents == 5000000
        assert vehicle.description == "Test vehicle"


class TestStockList:
    @respx.mock
    def test_list_returns_stock_vehicles(self, sync_client: CredereClient) -> None:
        route = respx.get(VEHICLES_URL).mock(
            return_value=httpx.Response(200, json=[SAMPLE_VEHICLE])
        )

        vehicles = sync_client.stock.list()

        assert route.called
        assert isinstance(vehicles, list)
        assert len(vehicles) == 1
        assert isinstance(vehicles[0], StockVehicle)
        assert vehicles[0].id == 1
        assert vehicles[0].price_cents == 5000000
        assert vehicles[0].description == "Test vehicle"


class TestStockUpdate:
    @respx.mock
    def test_update_returns_stock_vehicle(self, sync_client: CredereClient) -> None:
        url = f"{VEHICLES_URL}/1"
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json={"vehicle": SAMPLE_VEHICLE})
        )

        vehicle = sync_client.stock.update(1, SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(vehicle, StockVehicle)
        assert vehicle.id == 1
        assert vehicle.price_cents == 5000000
        assert vehicle.description == "Test vehicle"


class TestStockRemove:
    @respx.mock
    def test_remove_returns_stock_vehicle(self, sync_client: CredereClient) -> None:
        url = f"{VEHICLES_URL}/1/remove_from_stock"
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json={"vehicle": SAMPLE_VEHICLE})
        )

        vehicle = sync_client.stock.remove(1)

        assert route.called
        assert isinstance(vehicle, StockVehicle)
        assert vehicle.id == 1
        assert vehicle.price_cents == 5000000
        assert vehicle.description == "Test vehicle"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(VEHICLES_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.stock.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{VEHICLES_URL}/999/remove_from_stock"
        respx.put(url).mock(
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
            sync_client.stock.remove(999)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncStockCreate:
    @respx.mock
    async def test_async_create_returns_stock_vehicle(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.post(VEHICLES_URL).mock(
            return_value=httpx.Response(200, json={"vehicle": SAMPLE_VEHICLE})
        )

        vehicle = await async_client.stock.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(vehicle, StockVehicle)
        assert vehicle.id == 1
        assert vehicle.price_cents == 5000000
        assert vehicle.description == "Test vehicle"


class TestAsyncStockList:
    @respx.mock
    async def test_async_list_returns_stock_vehicles(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(VEHICLES_URL).mock(
            return_value=httpx.Response(200, json=[SAMPLE_VEHICLE])
        )

        vehicles = await async_client.stock.list()

        assert route.called
        assert isinstance(vehicles, list)
        assert len(vehicles) == 1
        assert isinstance(vehicles[0], StockVehicle)
        assert vehicles[0].id == 1
        assert vehicles[0].price_cents == 5000000
        assert vehicles[0].description == "Test vehicle"
