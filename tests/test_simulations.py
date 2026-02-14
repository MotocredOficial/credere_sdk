"""Tests for the Simulations resource (sync + async)."""

import json

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.simulations import (
    Simulation,
    SimulationConditionRequest,
    SimulationCreateRequest,
    SimulationVehicleRequest,
)

BASE_URL = "https://api.credere.com"
SIMULATIONS_URL = f"{BASE_URL}/v1/banks_api/simulations"
LIST_URL = f"{BASE_URL}/v1/proposal_simulations"

SAMPLE_CONDITION = {
    "id": 1,
    "installments": 48,
    "down_payment": 1000000,
    "financed_amount": 4000000,
    "created_at": "2024-01-15T10:00:00-03:00",
    "bank": {
        "id": 10,
        "febraban_code": "341",
        "name": "Itaú Unibanco",
        "nickname": "Itaú",
    },
    "success": True,
    "error": None,
    "interest_monthly": 1.49,
    "interest_annually": 19.41,
    "cet_monthly": 1.62,
    "cet_annually": 21.28,
    "first_installment_value": 120000,
    "last_installment_value": 118000,
    "amount_paid_in_financing": 5760000,
    "available": True,
    "credit_condition_code": "ABC123",
    "credit_condition_description": "Crédito aprovado",
    "process_task": {},
    "pre_approval_status": None,
    "reason": None,
}

SAMPLE_SIMULATION_RESPONSE = {
    "data": {
        "assets_value": 5000000,
        "conditions": [SAMPLE_CONDITION],
    }
}

SAMPLE_LIST_RESPONSE = {"data": [SAMPLE_SIMULATION_RESPONSE["data"]]}

SAMPLE_CREATE_DATA = SimulationCreateRequest(
    assets_value=5000000,
    documentation_value=50000,
    conditions=[
        SimulationConditionRequest(
            down_payment=1000000,
            financed_amount=4000000,
            installments=48,
        )
    ],
    retrieve_lead={"cpf_cnpj": "12345678900"},
    seller_cpf="98765432100",
    vehicle=SimulationVehicleRequest(
        asset_value=5000000,
        licensing_uf="SP",
        manufacture_year=2024,
        model_year=2024,
        vehicle_molicar_code="MOL123",
        zero_km=True,
    ),
)


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestSimulationsCreate:
    @respx.mock
    def test_create_simulation(self, sync_client: CredereClient) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = sync_client.simulations.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(sim, Simulation)
        assert sim.assets_value == 5000000
        assert sim.conditions is not None
        assert len(sim.conditions) == 1
        assert sim.conditions[0].id == 1
        assert sim.conditions[0].bank is not None
        assert sim.conditions[0].bank.febraban_code == "341"
        assert sim.conditions[0].success is True

    @respx.mock
    def test_create_sends_correct_body(self, sync_client: CredereClient) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sync_client.simulations.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        body = json.loads(request.content)
        assert "simulation" in body
        assert body["simulation"]["assets_value"] == 5000000
        assert body["simulation"]["seller_cpf"] == "98765432100"
        assert body["simulation"]["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(body["simulation"]["conditions"]) == 1
        assert body["simulation"]["vehicle"]["zero_km"] is True

    @respx.mock
    def test_create_sends_store_id_header(self, sync_client: CredereClient) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sync_client.simulations.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"


class TestSimulationsList:
    @respx.mock
    def test_list_simulations(self, sync_client: CredereClient) -> None:
        route = respx.get(LIST_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        sims = sync_client.simulations.list()

        assert route.called
        assert isinstance(sims, list)
        assert len(sims) == 1
        assert isinstance(sims[0], Simulation)
        assert sims[0].assets_value == 5000000
        assert sims[0].conditions is not None
        assert len(sims[0].conditions) == 1

    @respx.mock
    def test_list_uses_correct_path(self, sync_client: CredereClient) -> None:
        route = respx.get(LIST_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        sync_client.simulations.list()

        request = route.calls.last.request
        assert "/v1/proposal_simulations" in str(request.url)


class TestSimulationsGet:
    @respx.mock
    def test_get_simulation(self, sync_client: CredereClient) -> None:
        uuid = "abc-123-def"
        url = f"{SIMULATIONS_URL}/{uuid}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = sync_client.simulations.get(uuid)

        assert route.called
        assert isinstance(sim, Simulation)
        assert sim.assets_value == 5000000
        assert sim.conditions is not None
        assert sim.conditions[0].interest_monthly == 1.49


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestSimulationsErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(LIST_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.simulations.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{SIMULATIONS_URL}/nonexistent"
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
            sync_client.simulations.get("nonexistent")

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncSimulationsCreate:
    @respx.mock
    async def test_async_create_simulation(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = await async_client.simulations.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(sim, Simulation)
        assert sim.assets_value == 5000000
        assert sim.conditions is not None
        assert len(sim.conditions) == 1


class TestAsyncSimulationsList:
    @respx.mock
    async def test_async_list_simulations(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(LIST_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        sims = await async_client.simulations.list()

        assert route.called
        assert len(sims) == 1
        assert isinstance(sims[0], Simulation)


class TestAsyncSimulationsGet:
    @respx.mock
    async def test_async_get_simulation(self, async_client: AsyncCredereClient) -> None:
        uuid = "abc-123-def"
        url = f"{SIMULATIONS_URL}/{uuid}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = await async_client.simulations.get(uuid)

        assert route.called
        assert isinstance(sim, Simulation)
        assert sim.assets_value == 5000000


class TestAsyncSimulationsErrorMapping:
    @respx.mock
    async def test_async_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(LIST_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError):
            await async_client.simulations.list()

    @respx.mock
    async def test_async_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{SIMULATIONS_URL}/nonexistent"
        respx.get(url).mock(
            return_value=httpx.Response(
                404,
                json={
                    "error": {
                        "message": "Not found",
                        "status": 404,
                    }
                },
            )
        )

        with pytest.raises(NotFoundError):
            await async_client.simulations.get("nonexistent")
