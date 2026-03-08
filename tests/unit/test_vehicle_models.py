"""Tests for the Vehicle Models resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError
from credere.models.vehicle_models import VehicleModel, VehiclePrice

BASE_URL = "https://app.meucredere.com.br"
MODELS_URL = f"{BASE_URL}/api/v1/vehicle_models"
PRICES_URL = f"{BASE_URL}/api/v1/vehicle_prices"

SAMPLE_VEHICLE_MODEL = {
    "vehicle_model": {
        "object_type": "VehicleModel",
        "id": 1,
        "created_at": "2020-05-06T19:10:59.233-03:00",
        "updated_at": "2023-11-04T00:22:24.185-03:00",
        "name": "BIZ",
        "brand": "HONDA",
        "molicar_code": "00000000-0",
        "version": "110 i CBS - Basico",
        "year_end": 2024,
        "year_start": 2019,
        "active": True,
        "public_price_cents": 1100000,
        "public_price_as_string": "BRL",
        "publish": True,
        "fipe_code": "811138-3",
        "public_picture": "https://dcqotzwnlmq7s.cloudfront.net/5od0958jbdwlo61uq13t6jabhyatfear.png",
        "vehicle_brand": {"id": 103, "name": "HONDA"},
        "fuel": {
            "object_type": "Fuel",
            "id": 1,
            "created_at": "2013-12-25T16:42:44.693-02:00",
            "updated_at": "2013-12-25T16:42:44.693-02:00",
            "name": "Gasolina",
        },
        "vehicle_type": {"id": 2, "name": "Motos"},
    }
}

SAMPLE_VEHICLE_PRICE = {
    "vehicle_prices": [
        {
            "id": 1,
            "store_id": 42,
            "min_price_cents": 400000,
            "default_price_cents": 500000,
            "active": True,
            "created_at": "2012-06-30T16:12:59-03:00",
            "updated_at": "2016-03-26T23:41:28-03:00",
            "vehicle_model": {
                "id": 1,
                "name": "BIZ",
                "brand": "Honda",
                "molicar_code": "12345678-9",
                "version": "100 KS",
                "year_end": 2015,
                "year_start": 2012,
                "created_at": "2012-05-30T16:12:59-03:00",
                "updated_at": "2015-03-26T23:41:28-03:00",
                "fuel": {"id": 1, "name": "Gasolina"},
            },
            "store": {
                "id": 100,
                "name": "Loja A",
                "display_name": "Loja A",
                "uf": "RN",
                "limit_vehicle_prices": False,
                "created_at": "2012-05-30T16:12:59-03:00",
                "updated_at": "2018-03-26T23:41:28-03:00",
            },
        }
    ]
}

SAMPLE_VEHICLES_LIST_RESPONSE = {
    "vehicle_models": [SAMPLE_VEHICLE_MODEL["vehicle_model"]]
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestVehicleModelsList:
    @respx.mock
    def test_list_returns_vehicle_models(self, sync_client: CredereClient) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        result = sync_client.vehicle_models.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == 1
        assert result[0].brand == "HONDA"
        assert result[0].molicar_code == "00000000-0"
        assert result[0].active is True

    @respx.mock
    def test_list_sends_per_page_query_param(self, sync_client: CredereClient) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        sync_client.vehicle_models.list(per_page=5)

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("per_page") == "5"

    @respx.mock
    def test_list_sends_molicar_code_query_param(
        self, sync_client: CredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        sync_client.vehicle_models.list(molicar_code="00000000-0")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("molicar_code") == "00000000-0"

    @respx.mock
    def test_list_sends_fipe_code_query_param(self, sync_client: CredereClient) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        sync_client.vehicle_models.list(fipe_code="811138-3")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("fipe_code") == "811138-3"

    @respx.mock
    def test_list_omits_none_query_params(self, sync_client: CredereClient) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        sync_client.vehicle_models.list()

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert "per_page" not in sent_params
        assert "molicar_code" not in sent_params
        assert "fipe_code" not in sent_params


class TestVehicleModelsSearch:
    @respx.mock
    def test_search_returns_vehicle_model(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        result = sync_client.vehicle_models.search("Honda")

        assert route.called
        assert isinstance(result, VehicleModel)
        assert result.id == 1
        assert result.brand == "HONDA"
        assert result.molicar_code == "00000000-0"
        assert result.active is True

    @respx.mock
    def test_search_sends_q_query_param(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        sync_client.vehicle_models.search("Honda CG")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("q") == "Honda CG"

    @respx.mock
    def test_search_sends_extra_params(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        sync_client.vehicle_models.search("BIZ", custom_filter="active")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("q") == "BIZ"
        assert sent_params.get("custom_filter") == "active"


class TestVehicleModelsPrices:
    @respx.mock
    def test_prices_returns_vehicle_prices(self, sync_client: CredereClient) -> None:
        route = respx.get(PRICES_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_PRICE)
        )

        result = sync_client.vehicle_models.prices()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehiclePrice)
        assert result[0].id == 1
        assert result[0].store_id == 42
        assert result[0].min_price_cents == 400000
        assert result[0].default_price_cents == 500000
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
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        result = await async_client.vehicle_models.list()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == 1

    @respx.mock
    async def test_async_list_sends_per_page_query_param(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        await async_client.vehicle_models.list(per_page=5)

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("per_page") == "5"

    @respx.mock
    async def test_async_list_sends_molicar_code_query_param(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        await async_client.vehicle_models.list(molicar_code="00000000-0")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("molicar_code") == "00000000-0"

    @respx.mock
    async def test_async_list_sends_fipe_code_query_param(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        await async_client.vehicle_models.list(fipe_code="811138-3")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("fipe_code") == "811138-3"

    @respx.mock
    async def test_async_list_omits_none_query_params(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(MODELS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLES_LIST_RESPONSE)
        )

        await async_client.vehicle_models.list()

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert "per_page" not in sent_params
        assert "molicar_code" not in sent_params
        assert "fipe_code" not in sent_params


class TestAsyncVehicleModelsSearch:
    @respx.mock
    async def test_async_search_returns_vehicle_model(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        result = await async_client.vehicle_models.search("HONDA")

        assert route.called
        assert isinstance(result, VehicleModel)
        assert result.id == 1
        assert result.brand == "HONDA"

    @respx.mock
    async def test_async_search_sends_q_query_param(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        await async_client.vehicle_models.search("Honda CG")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("q") == "Honda CG"

    @respx.mock
    async def test_async_search_sends_extra_params(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{MODELS_URL}/search").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE_MODEL)
        )

        await async_client.vehicle_models.search("BIZ", custom_filter="active")

        assert route.called
        sent_params = dict(route.calls[0].request.url.params)
        assert sent_params.get("q") == "BIZ"
        assert sent_params.get("custom_filter") == "active"
