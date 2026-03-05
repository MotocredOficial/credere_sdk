"""Integration tests for the Proposal Attempts resource.

Requires an existing proposal. Set PROPOSAL_ID and SIMULATION_* constants below.

Run directly:
    python tests/integration/test_proposal_attempts.py
"""

import pytest

from credere.client import CredereClient
from credere.models.proposal_attempts import (
    ProposalAttemptData,
    ProposalAttemptRequest,
    ProposalAttemptResponse,
)
from credere.models.proposals import ProposalAttempt, ProposalData, ProposalResponse

from .config import STORE_ID

CUSTOMER_ID = 2472825  # Existing customer id
SELLER_ID = 42102  # real seller id from the reference JSON
SIMULATION_CONDITION_ID = 368339483  # from a real simulation condition
SIMULATION_UUID = "1a887757-d67c-4d96-8bd2-f41756e46c56"  # from a real simulation


@pytest.fixture(scope="module")
def created_proposal_for_attempt(sync_client: CredereClient) -> ProposalResponse:
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

    proposal = sync_client.proposals.create(proposal_data, store_id=STORE_ID)
    yield proposal
    sync_client.proposals.delete(proposal.id, store_id=STORE_ID)


@pytest.fixture
def created_proposal_attempt(
    sync_client: CredereClient, created_proposal_for_attempt: ProposalResponse
) -> ProposalAttemptResponse:
    proposal_attempt_data = ProposalAttemptData(
        proposal_id=created_proposal_for_attempt.id,
        proposal_attempt=ProposalAttemptRequest(
            simulation_condition_id=SIMULATION_CONDITION_ID,
            external_simulation_uuid=SIMULATION_UUID,
        ),
    )

    return sync_client.proposal_attempts.create(
        created_proposal_for_attempt.id, proposal_attempt_data, store_id=STORE_ID
    )


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_proposal_attempt(
    sync_client: CredereClient,
    created_proposal_attempt: ProposalAttemptResponse,
) -> None:
    assert isinstance(created_proposal_attempt, ProposalAttemptResponse)
    assert created_proposal_attempt.id
    print(f"  [OK] create_proposal_attempt — id={created_proposal_attempt.id}")


def test_get_proposal_attempt(
    sync_client: CredereClient,
    created_proposal_attempt: ProposalAttemptResponse,
    created_proposal_for_attempt: ProposalResponse,
) -> None:
    proposal_id = created_proposal_for_attempt.id
    proposal_attempt_id = created_proposal_attempt.id
    attempt = sync_client.proposal_attempts.get(
        proposal_id, proposal_attempt_id, store_id=STORE_ID
    )
    assert isinstance(attempt, ProposalAttemptResponse)
    assert str(attempt.id) == str(proposal_attempt_id)
    print(f"  [OK] get_proposal_attempt — id={attempt.id}")


def test_list_proposal_attempts(
    sync_client: CredereClient, created_proposal_for_attempt: ProposalResponse
) -> None:
    proposal_id = created_proposal_for_attempt.id
    attempts = sync_client.proposal_attempts.list(proposal_id, store_id=STORE_ID)
    assert isinstance(attempts, list)
    print(f"  [OK] list_proposal_attempts — {len(attempts)} attempt(s) returned")
