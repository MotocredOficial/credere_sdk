"""Tests for the Vehicle Models resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError
from credere.models.vehicle_models import VehicleModel, VehiclePrice

BASE_URL = "https://api.credere.com"
MODELS_URL = f"{BASE_URL}/v1/vehicle_models"
PRICES_URL = f"{BASE_URL}/v1/vehicle_prices"

SAMPLE_VEHICLE_MODEL = {
    "id": 1,
    "name": "Civic",
    "brand": "Honda",
    "molicar_code": "123456",
    "active": True,
}

SAMPLE_VEHICLE_PRICE = {
    "id": 1,
    "store_id": 42,
    "min_price_cents": 5000000,
    "default_price_cents": 6000000,
    "active": True,
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestVehicleModelsList:
    @respx.mock
    def test_list_returns_vehicle_models(self, sync_client: CredereClient) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(
                200, json={"vehicle_models": [SAMPLE_VEHICLE_MODEL]}
            )
        )

        result = sync_client.vehicle_models.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == 1
        assert result[0].name == "Civic"
        assert result[0].brand == "Honda"
        assert result[0].molicar_code == "123456"
        assert result[0].active is True


class TestVehicleModelsSearch:
    @respx.mock
    def test_search_returns_vehicle_model(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(
                200, json={"vehicle_model": SAMPLE_VEHICLE_MODEL}
            )
        )

        result = sync_client.vehicle_models.search("Civic")

        assert route.called
        assert isinstance(result, VehicleModel)
        assert result.id == 1
        assert result.name == "Civic"
        assert result.brand == "Honda"
        assert result.molicar_code == "123456"
        assert result.active is True


class TestVehicleModelsPrices:
    @respx.mock
    def test_prices_returns_vehicle_prices(self, sync_client: CredereClient) -> None:
        route = respx.get(PRICES_URL).mock(
            return_value=httpx.Response(
                200, json={"vehicle_prices": [SAMPLE_VEHICLE_PRICE]}
            )
        )

        result = sync_client.vehicle_models.prices()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehiclePrice)
        assert result[0].id == 1
        assert result[0].store_id == 42
        assert result[0].min_price_cents == 5000000
        assert result[0].default_price_cents == 6000000
        assert result[0].active is True


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(MODELS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.vehicle_models.list()

        assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncVehicleModelsList:
    @respx.mock
    async def test_async_list_returns_vehicle_models(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(
                200, json={"vehicle_models": [SAMPLE_VEHICLE_MODEL]}
            )
        )

        result = await async_client.vehicle_models.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == 1
        assert result[0].name == "Civic"


class TestAsyncVehicleModelsSearch:
    @respx.mock
    async def test_async_search_returns_vehicle_model(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(
                200, json={"vehicle_model": SAMPLE_VEHICLE_MODEL}
            )
        )

        result = await async_client.vehicle_models.search("Civic")

        assert route.called
        assert isinstance(result, VehicleModel)
        assert result.id == 1
        assert result.name == "Civic"
