"""Tests for the Proposal Attempts resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.proposal_attempts import (
    ProposalAttempt,
    ProposalAttemptCreateRequest,
)

BASE_URL = "https://api.credere.com"
PROPOSAL_ID = "abc-123"
ATTEMPTS_URL = f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/proposal_attempts"

SAMPLE_ATTEMPT_RESPONSE = {
    "data": {
        "id": 1,
        "created_at": "2024-01-15T10:00:00-03:00",
        "updated_at": "2024-01-15T10:00:00-03:00",
    }
}

SAMPLE_LIST_RESPONSE = {"data": [SAMPLE_ATTEMPT_RESPONSE["data"]]}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestProposalAttemptsCreate:
    @respx.mock
    def test_create_proposal_attempt(self, sync_client: CredereClient) -> None:
        route = respx.post(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = sync_client.proposal_attempts.create(
            PROPOSAL_ID, ProposalAttemptCreateRequest()
        )

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1


class TestProposalAttemptsList:
    @respx.mock
    def test_list_proposal_attempts(self, sync_client: CredereClient) -> None:
        route = respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = sync_client.proposal_attempts.list(PROPOSAL_ID)

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProposalAttempt)
        assert result[0].id == 1


class TestProposalAttemptsGet:
    @respx.mock
    def test_get_proposal_attempt(self, sync_client: CredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = sync_client.proposal_attempts.get(PROPOSAL_ID, 1)

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1


class TestProposalAttemptsUpdate:
    @respx.mock
    def test_update_proposal_attempt(self, sync_client: CredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1"
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = sync_client.proposal_attempts.update(
            PROPOSAL_ID, 1, ProposalAttemptCreateRequest()
        )

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1


class TestProposalAttemptsPerformAction:
    @respx.mock
    def test_perform_action_approve(self, sync_client: CredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1/approve"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = sync_client.proposal_attempts.perform_action(PROPOSAL_ID, 1, "approve")

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.proposal_attempts.list(PROPOSAL_ID)

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        respx.get(ATTEMPTS_URL).mock(
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
            sync_client.proposal_attempts.list(PROPOSAL_ID)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncProposalAttemptsCreate:
    @respx.mock
    async def test_async_create_proposal_attempt(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.post(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = await async_client.proposal_attempts.create(
            PROPOSAL_ID, ProposalAttemptCreateRequest()
        )

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1


class TestAsyncProposalAttemptsList:
    @respx.mock
    async def test_async_list_proposal_attempts(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        result = await async_client.proposal_attempts.list(PROPOSAL_ID)

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProposalAttempt)


class TestAsyncProposalAttemptsGet:
    @respx.mock
    async def test_async_get_proposal_attempt(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{ATTEMPTS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_RESPONSE)
        )

        result = await async_client.proposal_attempts.get(PROPOSAL_ID, 1)

        assert route.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1
