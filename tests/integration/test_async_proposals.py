"""Async integration tests for the Proposals resource.

Requires a customer and simulation to already exist.
Set CUSTOMER_ID and SIMULATION_* constants below.
"""

import pytest

from credere.client import AsyncCredereClient
from credere.models.proposals import ProposalAttempt, ProposalData, ProposalResponse

from .config import STORE_ID

CUSTOMER_ID = 2472825
SELLER_ID = 42102
SIMULATION_CONDITION_ID = 368339483
SIMULATION_UUID = "1a887757-d67c-4d96-8bd2-f41756e46c56"


@pytest.fixture
async def created_proposal(async_client: AsyncCredereClient) -> ProposalResponse:
    proposal_data = ProposalData(
        customer_id=CUSTOMER_ID,
        store_id=STORE_ID,
        seller_id=SELLER_ID,
        commercial=False,
        km_mileage=10000,
        licensing_city="Fortaleza",
        chassi_code="1HGCM82633A004352",
        renavam_code="123456789",
        color="Vermelho",
        licensing_uf="NY",
        proposal_attemps=[
            ProposalAttempt(
                simulation_condition_id=SIMULATION_CONDITION_ID,
                external_simulation_uuid=SIMULATION_UUID,
            )
        ],
    )

    proposal = await async_client.proposals.create(proposal_data, store_id=STORE_ID)
    yield proposal
    await async_client.proposals.delete(proposal.id, store_id=STORE_ID)


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


async def test_create_proposal(created_proposal: ProposalResponse) -> None:
    assert isinstance(created_proposal, ProposalResponse)
    assert created_proposal.id
    print(f"  [OK] create_proposal — id={created_proposal.id}")


async def test_get_proposal(
    async_client: AsyncCredereClient, created_proposal: ProposalResponse
) -> None:
    proposal = await async_client.proposals.get(created_proposal.id, store_id=STORE_ID)
    assert isinstance(proposal, ProposalResponse)
    assert proposal.id == created_proposal.id
    print(f"  [OK] get_proposal — id={proposal.id}")


async def test_list_proposals(
    async_client: AsyncCredereClient, created_proposal: ProposalResponse
) -> None:
    proposals = await async_client.proposals.list(store_id=STORE_ID)
    assert isinstance(proposals, list)
    print(f"  [OK] list_proposals — {len(proposals)} proposal(s) returned")


async def test_activity_log(
    async_client: AsyncCredereClient, created_proposal: ProposalResponse
) -> None:
    log = await async_client.proposals.activity_log(
        created_proposal.id, store_id=STORE_ID
    )
    assert isinstance(log, dict)
    print(f"  [OK] activity_log — {len(log)} event(s) returned")
