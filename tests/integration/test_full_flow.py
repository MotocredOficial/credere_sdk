"""Integration test covering the full flow:
    lead → simulation → customer → proposal → proposal_attempt

Each step receives its inputs from the previous one.
Fill in the TODO values with real data before running.

Run directly:
    python tests/integration/test_full_flow.py
"""

from credere.client import CredereClient
from credere.models.customers import CustomerData, CustomerResponse, Email, Phone
from credere.models.leads import Address, LeadData, LeadResponse
from credere.models.proposal_attempts import (
    ProposalAttemptData,
    ProposalAttemptRequest,
    ProposalAttemptResponse,
)
from credere.models.proposals import ProposalAttempt, ProposalData, ProposalResponse
from credere.models.simulations import (
    Condition,
    RetrieveLead,
    SimulationData,
    SimulationResponse,
    Vehicle,
)

from config import API_KEY, BASE_URL, STORE_ID

# ---------------------------------------------------------------------------
# Shared fake data — replace TODOs with real values before running
# ---------------------------------------------------------------------------

LEAD_CPF = "000.000.000-00"  # TODO: replace with a valid CPF
SELLER_ID = 0  # TODO: replace with a real seller id
BANK_FEBRABAN_CODE = "000"  # TODO: replace with a real febraban code
BANK_LIST = [BANK_FEBRABAN_CODE]
VEHICLE_MODEL_ID = "00000000-0000-0000-0000-000000000000"  # TODO: real vehicle model UUID

# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------


def step_create_lead(client: CredereClient) -> LeadResponse:
    data = LeadData(
        cpf_cnpj=LEAD_CPF,
        name="Nome Teste Flow",
        birthdate="1990-01-01",
        email="flow@email.com",
        phone_number="(00) 90000-0000",
        monthly_income=300000,
        has_cnh=True,
        retrieve_gender="M",
        retrieve_occupation="11",
        retrieve_profession="administrador",
        address=Address(
            zip_code="00000-000",
            city="Cidade Teste",
            state="SP",
            district="Bairro Teste",
            street="Rua Teste",
            number="123",
        ),
    )
    lead = client.leads.create(data, store_id=STORE_ID)
    assert isinstance(lead, LeadResponse)
    assert lead.cpf_cnpj is not None
    print(f"  [1/5] Lead created — id={lead.id}, cpf_cnpj={lead.cpf_cnpj}")
    return lead


def step_create_simulation(client: CredereClient, lead: LeadResponse) -> SimulationResponse:
    data = SimulationData(
        process_bank_suggested_conditions=True,
        process_credere_suggested_conditions=False,
        retrieve_lead=RetrieveLead(cpf_cnpj=lead.cpf_cnpj),
        bank_febraban_codes=[BANK_FEBRABAN_CODE],
        vehicle=Vehicle(
            credere_vehicle_model_id=VEHICLE_MODEL_ID,
            licensing_uf="SP",
            licensing_city="São Paulo",
            manufacture_year=2023,
            model_year=2024,
            asset_value=1500000,
            zero_km=True,
        ),
        conditions=[
            Condition(
                installments=36,
                down_payment=300000,
                bank_febraban_code=BANK_FEBRABAN_CODE,
            ),
        ],
    )
    simulation = client.simulations.create(data, store_id=STORE_ID)
    assert isinstance(simulation, SimulationResponse)
    assert simulation.simulation_id
    print(f"  [2/5] Simulation created — simulation_id={simulation.simulation_id}")
    return simulation


def step_create_customer(client: CredereClient, lead: LeadResponse) -> CustomerResponse:
    data = CustomerData(
        cpf=lead.cpf_cnpj,
        name=lead.name or "Nome Cliente Flow",
        born_at=lead.birthdate or "1990-01-01",
        emails=[Email(address="flow@email.com")],
        phones=[Phone(code=11, number=900000000)],
        document_type="cpf",
        rg="0000000",
        rg_date="2010-01-01",
        rg_issuing="SSP",
        mother="Nome Mae Teste",
        marital_status_id=1,
        genre_id=1,
        nationality="brasileira",
        place_of_birth="São Paulo",
    )
    customer = client.customers.create(data, BANK_LIST, store_id=STORE_ID)
    assert isinstance(customer, CustomerResponse)
    assert customer.id
    print(f"  [3/5] Customer created — id={customer.id}, name={customer.name}")
    return customer


def step_create_proposal(
    client: CredereClient,
    customer: CustomerResponse,
    simulation: SimulationResponse,
) -> ProposalResponse:
    # The simulation raw_response contains the conditions; pick the first one.
    # TODO: adjust the key path to match the real API response structure.
    conditions = simulation.raw_response.get("conditions", [])
    first_condition = conditions[0] if conditions else {}
    condition_id: int = first_condition.get("id", 0)  # TODO: verify key name

    data = ProposalData(
        customer_id=customer.id,
        store_id=STORE_ID,
        seller_id=SELLER_ID,
        commercial=False,
        proposal_attempts=[
            ProposalAttempt(
                simulation_condition_id=condition_id,
                external_simulation_uuid=simulation.simulation_id,
            )
        ],
        km_mileage=0,
        license_plate_code="AAA0000",
        color="Preto",
        licensing_uf="SP",
        licensing_city="São Paulo",
    )
    proposal = client.proposals.create(data, store_id=STORE_ID)
    assert isinstance(proposal, ProposalResponse)
    assert proposal.id
    print(f"  [4/5] Proposal created — id={proposal.id}, state={proposal.state}")
    return proposal


def step_create_proposal_attempt(
    client: CredereClient,
    proposal: ProposalResponse,
    simulation: SimulationResponse,
) -> ProposalAttemptResponse:
    proposal_id_str = str(proposal.id)

    # Reuse the same condition from the proposal's embedded attempt.
    condition_id: int = proposal.proposal_attempt.simulation_condition_id

    data = ProposalAttemptData(
        proposal_id=proposal.id,
        proposal_attempt=ProposalAttemptRequest(
            simulation_condition_id=condition_id,
            external_simulation_uuid=simulation.simulation_id,
        ),
    )
    attempt = client.proposal_attempts.create(proposal_id_str, data, store_id=STORE_ID)
    assert isinstance(attempt, ProposalAttemptResponse)
    assert attempt.id
    print(f"  [5/5] Proposal Attempt created — id={attempt.id}, state={attempt.state}")
    return attempt


# ---------------------------------------------------------------------------
# Full flow runner
# ---------------------------------------------------------------------------


def run_full_flow() -> None:
    with CredereClient(api_key=API_KEY, base_url=BASE_URL, store_id=STORE_ID) as client:
        print("=== Full Flow integration test ===")
        print("  lead → simulation → customer → proposal → proposal_attempt\n")

        lead = step_create_lead(client)
        simulation = step_create_simulation(client, lead)
        customer = step_create_customer(client, lead)
        proposal = step_create_proposal(client, customer, simulation)
        attempt = step_create_proposal_attempt(client, proposal, simulation)

        print("\n--- Summary ---")
        print(f"  Lead id            : {lead.id}")
        print(f"  Simulation id      : {simulation.simulation_id}")
        print(f"  Customer id        : {customer.id}")
        print(f"  Proposal id        : {proposal.id}")
        print(f"  Proposal Attempt id: {attempt.id}")
        print("\n=== Full Flow test passed ===")


if __name__ == "__main__":
    run_full_flow()
