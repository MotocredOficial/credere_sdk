"""Async integration tests for the Vehicle Models resource."""

import pytest

from credere.client import AsyncCredereClient
from credere.models.vehicle_models import VehicleModel, VehiclePrice

from .config import STORE_ID

MOLICAR_CODE = "01907514-5"

pytestmark = pytest.mark.asyncio


async def test_list_vehicle_models(async_client: AsyncCredereClient) -> None:
    models = await async_client.vehicle_models.list(store_id=STORE_ID)
    assert isinstance(models, list)
    assert models, "Expected at least one vehicle model in the list"
    assert all(isinstance(m, VehicleModel) for m in models)
    print(f"  [OK] list_vehicle_models — {len(models)} model(s) returned")


async def test_list_vehicle_models_per_page(async_client: AsyncCredereClient) -> None:
    per_page = 3
    models = await async_client.vehicle_models.list(
        store_id=STORE_ID, per_page=per_page
    )
    assert isinstance(models, list)
    assert len(models) <= per_page
    assert all(isinstance(m, VehicleModel) for m in models)
    print(
        f"  [OK] list_vehicle_models (per_page={per_page})"
        f" — {len(models)} model(s) returned"
    )


async def test_list_vehicle_models_with_molicar_code(
    async_client: AsyncCredereClient,
) -> None:
    models = await async_client.vehicle_models.list(
        molicar_code=MOLICAR_CODE, store_id=STORE_ID
    )
    assert isinstance(models, list)
    assert all(isinstance(m, VehicleModel) for m in models)
    assert all(model.molicar_code == MOLICAR_CODE for model in models)
    print(
        f"  [OK] list_vehicle_models (molicar_code={MOLICAR_CODE})"
        f" — {len(models)} model(s) returned"
    )


async def test_search_vehicle_model(async_client: AsyncCredereClient) -> None:
    model = await async_client.vehicle_models.search("Honda CG", store_id=STORE_ID)
    assert isinstance(model, VehicleModel)
    assert model.id
    print(f"  [OK] search_vehicle_model — id={model.id}, name={model.name}")


async def test_list_vehicle_prices(async_client: AsyncCredereClient) -> None:
    prices = await async_client.vehicle_models.prices(store_id=STORE_ID)
    assert isinstance(prices, list)
    print(f"  [OK] list_vehicle_prices — {len(prices)} price(s) returned")


@pytest.mark.skipif(STORE_ID == 0, reason="STORE_ID not configured")
async def test_list_vehicle_prices_with_store(async_client: AsyncCredereClient) -> None:
    prices = await async_client.vehicle_models.prices(store_id=STORE_ID)
    assert isinstance(prices, list)
    for price in prices:
        assert isinstance(price, VehiclePrice)
    print(
        f"  [OK] list_vehicle_prices (store_id={STORE_ID})"
        f" — {len(prices)} price(s) returned"
    )
