"""Integration tests for the Proposal Attempts resource.

Requires an existing proposal. Set PROPOSAL_ID and SIMULATION_* constants below.

Run directly:
    python tests/integration/test_proposal_attempts.py
"""

from config import API_KEY, BASE_URL, STORE_ID

from credere.client import CredereClient
from credere.models.proposal_attempts import (
    ProposalAttemptData,
    ProposalAttemptRequest,
    ProposalAttemptResponse,
)

# ---------------------------------------------------------------------------
# Fake data — replace with real values before running
# ---------------------------------------------------------------------------

PROPOSAL_ID = (
    "00000000-0000-0000-0000-000000000000"  # TODO: replace with a real proposal id
)
PROPOSAL_INT_ID = 0  # TODO: integer id of the proposal above
SIMULATION_CONDITION_ID = 0  # TODO: from a real simulation condition
SIMULATION_UUID = "00000000-0000-0000-0000-000000000000"  # TODO: from a real simulation

ATTEMPT_DATA = ProposalAttemptData(
    proposal_id=PROPOSAL_INT_ID,
    proposal_attempt=ProposalAttemptRequest(
        simulation_condition_id=SIMULATION_CONDITION_ID,
        external_simulation_uuid=SIMULATION_UUID,
    ),
)

# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_proposal_attempt(client: CredereClient) -> ProposalAttemptResponse:
    attempt = client.proposal_attempts.create(
        PROPOSAL_ID, ATTEMPT_DATA, store_id=STORE_ID
    )
    assert isinstance(attempt, ProposalAttemptResponse)
    assert attempt.id
    print(f"  [OK] create_proposal_attempt — id={attempt.id}, state={attempt.state}")
    return attempt


def test_get_proposal_attempt(
    client: CredereClient, attempt_id: str
) -> ProposalAttemptResponse:
    attempt = client.proposal_attempts.get(PROPOSAL_ID, attempt_id, store_id=STORE_ID)
    assert isinstance(attempt, ProposalAttemptResponse)
    assert str(attempt.id) == attempt_id
    print(f"  [OK] get_proposal_attempt — id={attempt.id}")
    return attempt


def test_list_proposal_attempts(client: CredereClient) -> list[ProposalAttemptResponse]:
    attempts = client.proposal_attempts.list(PROPOSAL_ID, store_id=STORE_ID)
    assert isinstance(attempts, list)
    print(f"  [OK] list_proposal_attempts — {len(attempts)} attempt(s) returned")
    return attempts


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_all() -> None:
    with CredereClient(api_key=API_KEY, base_url=BASE_URL, store_id=STORE_ID) as client:
        print("=== Proposal Attempts integration tests ===")
        attempt = test_create_proposal_attempt(client)
        attempt_id = str(attempt.id)
        test_get_proposal_attempt(client, attempt_id)
        test_list_proposal_attempts(client)
        print("=== All Proposal Attempts tests passed ===\n")


if __name__ == "__main__":
    run_all()
