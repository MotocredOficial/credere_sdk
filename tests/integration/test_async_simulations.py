"""Async integration tests for the Simulations resource.

Depends on an existing lead (LEAD_CPF must be a valid lead in the system).
"""

import pytest

from credere.client import AsyncCredereClient
from credere.models.simulations import (
    Condition,
    RetrieveLead,
    SimulationData,
    SimulationResponse,
    Vehicle,
)

from .config import EXISTING_CPF, SELLER_CPF, STORE_ID


@pytest.fixture
def simulation_data() -> SimulationData:
    return SimulationData(
        process_bank_suggested_conditions=True,
        process_credere_suggested_conditions=False,
        seller_cpf=SELLER_CPF,
        retrieve_lead=RetrieveLead(cpf_cnpj=EXISTING_CPF),
        vehicle=Vehicle(
            vehicle_molicar_code="01907514-5",
            licensing_uf="RN",
            licensing_city="Natal",
            manufacture_year=2021,
            model_year=2021,
            asset_value=1000000,
            zero_km=False,
        ),
        conditions=[
            Condition(
                installments=12,
                down_payment=500000,
                min_return=0,
                max_return=5,
            ),
            Condition(
                installments=24,
                down_payment=500000,
                min_return=0,
                max_return=5,
            ),
            Condition(
                installments=36,
                down_payment=500000,
                min_return=0,
                max_return=5,
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


async def test_create_simulation(
    async_client: AsyncCredereClient, simulation_data: SimulationData
) -> None:
    simulation = await async_client.simulations.create(simulation_data, store_id=STORE_ID)
    assert isinstance(simulation, SimulationResponse)
    assert simulation.simulation_id
    print(f"  [OK] create_simulation — simulation_id={simulation.simulation_id}")


async def test_get_simulation(async_client: AsyncCredereClient) -> None:
    simulation_id = "139bd5cc-5bef-459b-abba-07a11754b142"
    simulation = await async_client.simulations.get(simulation_id, store_id=STORE_ID)
    assert isinstance(simulation, SimulationResponse)
    assert simulation.simulation_id == simulation_id
    assert simulation.raw_response is not None
    print(f"  [OK] get_simulation — simulation_id={simulation.simulation_id}")


async def test_list_simulations(async_client: AsyncCredereClient) -> None:
    simulations = await async_client.simulations.list(store_id=STORE_ID)
    assert isinstance(simulations, list)
    assert len(simulations) > 0
    print(f"  [OK] list_simulations — {len(simulations)} simulation(s) returned")
