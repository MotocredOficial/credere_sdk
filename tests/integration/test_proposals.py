"""Integration tests for the Proposals resource.

Requires a customer and simulation to already exist.
Set CUSTOMER_ID and SIMULATION_* constants below.

Run directly:
    python tests/integration/test_proposals.py
"""

import pytest

from credere.client import CredereClient
from credere.models.proposals import ProposalAttempt, ProposalData, ProposalResponse

from .config import STORE_ID

# ---------------------------------------------------------------------------
# Fake data — replace with real values before running
# ---------------------------------------------------------------------------

CUSTOMER_ID = 2472825  # TODO: replace with a real customer id
SELLER_ID = 42102  # TODO: replace with a real seller id
SIMULATION_CONDITION_ID = 368339483  # TODO: from a real simulation condition
SIMULATION_UUID = "1a887757-d67c-4d96-8bd2-f41756e46c56"  # TODO: from a real simulation


@pytest.fixture
def created_proposal(sync_client: CredereClient) -> ProposalResponse:
    proposal_data = ProposalData(
        customer_id=CUSTOMER_ID,
        store_id=STORE_ID,
        seller_id=SELLER_ID,
        commercial=False,
        km_mileage=10000,
        licensing_city="New York",
        chassi_code="1HGCM82633A004352",
        renavam_codes="123456789",
        color="Vermelho",
        licensing_uf="NY",
        proposal_attempts=[
            ProposalAttempt(
                simulation_condition_id=SIMULATION_CONDITION_ID,
                external_simulation_uuid=SIMULATION_UUID,
            )
        ],
    )

    proposal = sync_client.proposals.create(proposal_data, store_id=STORE_ID)
    yield proposal
    sync_client.proposals.delete(proposal.id, store_id=STORE_ID)


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_proposal(created_proposal) -> None:
    assert isinstance(created_proposal, ProposalResponse)
    assert created_proposal.id
    print(
        f"""
        [OK] create_proposal — id={created_proposal.id}, state={created_proposal.state}
        """
    )


def test_get_proposal(sync_client: CredereClient, created_proposal) -> None:
    proposal = sync_client.proposals.get(created_proposal.id, store_id=STORE_ID)
    assert isinstance(proposal, ProposalResponse)
    assert str(proposal.id) == created_proposal.id
    print(f"  [OK] get_proposal — id={proposal.id}")


def test_list_proposals(sync_client: CredereClient, created_proposal) -> None:
    proposals = sync_client.proposals.list(store_id=STORE_ID)
    assert isinstance(proposals, list)
    print(f"  [OK] list_proposals — {len(proposals)} proposal(s) returned")


def test_activity_log(sync_client: CredereClient, created_proposal) -> None:
    log = sync_client.proposals.activity_log(created_proposal.id, store_id=STORE_ID)
    assert isinstance(log, list)
    print(f"  [OK] activity_log — {len(log)} event(s) returned")
