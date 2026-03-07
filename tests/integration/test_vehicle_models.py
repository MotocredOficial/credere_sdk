"""Integration tests for the Vehicle Models resource.

Run directly:
    python tests/integration/test_vehicle_models.py
"""

import pytest

from credere.client import CredereClient
from credere.models.vehicle_models import VehicleModel, VehiclePrice

from .config import STORE_ID

MOLICAR_CODE = "01907514-5"


def test_list_vehicle_models(sync_client: CredereClient) -> None:
    models = sync_client.vehicle_models.list(store_id=STORE_ID)
    assert isinstance(models, list)
    assert isinstance(models[0], VehicleModel)
    print(f"  [OK] list_vehicle_models — {len(models)} model(s) returned")


def test_list_9999_vehicles_models(sync_client: CredereClient) -> None:
    models = sync_client.vehicle_models.list(store_id=STORE_ID, per_page=9999)
    assert isinstance(models, list)
    assert len(models) <= 9999
    assert any(model.brand.lower() == "avelloz" for model in models)
    print(f"  [OK] list_vehicle_models (limit=9999) — {len(models)} model(s) returned")


def test_list_vehicle_models_with_molicar_code(sync_client: CredereClient) -> None:
    models = sync_client.vehicle_models.list(
        molicar_code=MOLICAR_CODE, store_id=STORE_ID
    )
    assert isinstance(models, list)
    print(
        f"  [OK] list_vehicle_models (molicar_code={MOLICAR_CODE}) — {len(models)} model(s) returned"
    )


def test_search_vehicle_model(sync_client: CredereClient) -> None:
    model = sync_client.vehicle_models.search("Honda CG", store_id=STORE_ID)
    assert isinstance(model, VehicleModel)
    assert model.id
    print(f"  [OK] search_vehicle_model — id={model.id}, name={model.name}")


def test_list_vehicle_prices(sync_client: CredereClient) -> None:
    prices = sync_client.vehicle_models.prices(store_id=STORE_ID)
    assert isinstance(prices, list)
    print(f"  [OK] list_vehicle_prices — {len(prices)} price(s) returned")


@pytest.mark.skipif(STORE_ID == 0, reason="STORE_ID not configured")
def test_list_vehicle_prices_with_store(sync_client: CredereClient) -> None:
    prices = sync_client.vehicle_models.prices(store_id=STORE_ID)
    assert isinstance(prices, list)
    for price in prices:
        assert isinstance(price, VehiclePrice)
    print(
        f"  [OK] list_vehicle_prices (store_id={STORE_ID}) — {len(prices)} price(s) returned"
    )
