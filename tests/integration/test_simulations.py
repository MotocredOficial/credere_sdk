"""Integration tests for the Simulations resource.

Depends on an existing lead (LEAD_CPF must be a valid lead in the system).

Run directly:
    python tests/integration/test_simulations.py
"""

import pytest

from credere.client import CredereClient
from credere.models.leads import Address, LeadData
from credere.models.simulations import (
    Condition,
    RetrieveLead,
    SimulationData,
    SimulationResponse,
    Vehicle,
)

from .config import CLIENT_CPF, SELLER_CPF, STORE_ID

LEAD_CPF = CLIENT_CPF


@pytest.fixture
def simulation_data() -> SimulationData:
    return SimulationData(
        process_bank_suggested_conditions=True,
        process_credere_suggested_conditions=False,
        seller_cpf=SELLER_CPF,
        retrieve_lead=RetrieveLead(cpf_cnpj=LEAD_CPF),
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
            ),
            Condition(
                installments=24,
                down_payment=500000,
            ),
            Condition(
                installments=36,
                down_payment=500000,
            ),
        ],
    )


@pytest.fixture
def created_lead(sync_client: CredereClient) -> None:
    lead_data = LeadData(
        cpf_cnpj=LEAD_CPF,
        name="sync_client name",
        birthdate="1970-01-01",
        email="cliente@email.com",
        phone_number="(84) 90000-0000",
        monthly_income=900000,
        has_cnh=True,
        retrieve_gender="F",
        retrieve_occupation="11",
        retrieve_profession="administrador",
        address=Address(
            zip_code="59075-810",
            city="Natal",
            state="RN",
            district="Lagoa Nova",
            street="Av Amintas Barros",
            number="3700, Sala 409 Bloco A",
            complement="Edif Corporate Tower Edif Center-Trade",
        ),
    )

    lead = sync_client.leads.create(lead_data, store_id=STORE_ID)
    yield lead
    sync_client.leads.delete(LEAD_CPF, store_id=STORE_ID)


def test_create_simulation(sync_client, simulation_data, created_lead) -> None:
    simulation = sync_client.simulations.create(simulation_data, store_id=STORE_ID)
    assert isinstance(simulation, SimulationResponse)
    assert simulation.simulation_id
    print(f"  [OK] create_simulation — simulation_id={simulation.simulation_id}")


def test_get_simulation(sync_client) -> None:
    simulation_id = "139bd5cc-5bef-459b-abba-07a11754b142"
    simulation = sync_client.simulations.get(simulation_id, store_id=STORE_ID)
    assert isinstance(simulation, SimulationResponse)
    assert simulation.simulation_id == simulation_id
    assert simulation.raw_response is not None
    print(f"  [OK] get_simulation — simulation_id={simulation.simulation_id}")


def test_list_simulations(sync_client) -> None:
    simulations = sync_client.simulations.list(store_id=STORE_ID)
    assert isinstance(simulations, list)
    assert len(simulations) > 0

    print(f"  [OK] list_simulations — {len(simulations)} simulation(s) returned")
