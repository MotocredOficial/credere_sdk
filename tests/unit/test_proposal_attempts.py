"""Tests for the Proposal Attempts resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.proposal_attempts import (
    ProposalAttemptData,
    ProposalAttemptResponse,
)

BASE_URL = "https://app.meucredere.com.br"
PROPOSAL_ID = 1
ATTEMPTS_URL = f"{BASE_URL}/api/v1/proposals/{PROPOSAL_ID}/proposal_attempts"

SAMPLE_CREATE_REQUEST = {
    "proposal_id": 1,
    "proposal_attempt": {
        "simulation_condition_id": 1,
        "external_simulation_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    },
}

SAMPLE_PROPOSAL_ATTEMPT_RESPONSE = {
    "object_type": "ProposalAttemp",
    "id": 1,
    "created_at": "2022-01-01T00:00:00.000-00:00",
    "updated_at": "2022-01-01T00:00:00.000-00:00",
    "active": True,
    "bank": {
        "id": 116,
        "name": "Itaú Unibanco S.A.",
        "tradename": "Itaú",
        "febraban_code": "341",
    },
    "input_financing_in_cents": 1000000,
    "plan": {"return": "1", "return_offset": None},
    "quota_in_cents": 10000,
    "state": "checagem",
    "table": {"description": "TABLE DESCRIPTION"},
    "term_financing": 12,
    "value_in_cents": 1000000,
    "obs": None,
    "value_of_the_license_plate_in_cents": 0,
    "financed_amount_in_cents": 1000000,
    "coefficient": None,
    "has_license_plate": False,
    "first_payment_in_days": 30,
    "funding_type": {"id": 1, "name": "CDC"},
    "payment_type": {"id": 1, "name": "Carnê"},
    "input_origin": 1,
    "application": {"id": 1, "name": "Grupo X"},
    "external_simulation_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "simulation_condition_id": 1,
    "external_proposal_uuid": "ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj",
    "integration_error": {
        "error": "",
        "message": "translation missing: pt.integration_error.message",
        "error_details": "",
    },
    "state_rank": 1,
    "bank_proposal_identifier": "kkkkkkkk-llll-mmmm-nnnn-oooooooooooo",
    "honda_id": "kkkkkkkk-llll-mmmm-nnnn-oooooooooooo",
    "simulation_pre_approval_status": 1,
    "fixed_installments": True,
    "cet_monthly": 1,
    "cet_annually": 10,
    "return_value_cents": None,
    "formalization_state": None,
    "formalization": None,
    "replaced_by_proposal_attempt_id": None,
    "replaces_proposal_attempt_id": None,
    "has_accessory": False,
    "value_of_the_accessory_in_cents": 0,
    "expenses": [
        {
            "object_type": "ExpenseInfo",
            "id": 1,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "value_in_cents": 0,
            "credere_type": "register_rate",
            "description": None,
            "expense": None,
        },
        {
            "object_type": "ExpenseInfo",
            "id": 2,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "value_in_cents": 10000,
            "credere_type": "contract_record_rate",
            "description": None,
            "expense": None,
        },
        {
            "object_type": "ExpenseInfo",
            "id": 3,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "value_in_cents": 10000,
            "credere_type": "property_valuation_rate",
            "description": None,
            "expense": None,
        },
        {
            "object_type": "ExpenseInfo",
            "id": 4,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "value_in_cents": 10000,
            "credere_type": "iof_value",
            "description": None,
            "expense": None,
        },
        {
            "object_type": "ExpenseInfo",
            "id": 5,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "value_in_cents": 10000,
            "credere_type": "spf",
            "description": None,
            "expense": None,
        },
    ],
    "payment_flow": [
        {"installment_number": 12, "value_cents": 10000},
        {"installment_number": 11, "value_cents": 10000},
        {"installment_number": 10, "value_cents": 10000},
        {"installment_number": 9, "value_cents": 10000},
        {"installment_number": 8, "value_cents": 10000},
        {"installment_number": 7, "value_cents": 10000},
        {"installment_number": 6, "value_cents": 10000},
        {"installment_number": 5, "value_cents": 10000},
        {"installment_number": 4, "value_cents": 10000},
        {"installment_number": 3, "value_cents": 10000},
        {"installment_number": 2, "value_cents": 10000},
        {"installment_number": 1, "value_cents": 10000},
    ],
}

SAMPLE_ATTEMPT_LIST_REPONSE = {"proposal_attempts": [SAMPLE_PROPOSAL_ATTEMPT_RESPONSE]}
SAMPLE_ATTEMPT_CREATE_RESPONSE = {"proposal_attempt": SAMPLE_PROPOSAL_ATTEMPT_RESPONSE}
SAMPLE_ATTEMPT_GET_RESPONSE = SAMPLE_ATTEMPT_CREATE_RESPONSE


class TestProposalAttemptsCreate:
    @respx.mock
    def test_create_proposal_attempt(self, sync_client: CredereClient) -> None:
        proposal_attempt = ProposalAttemptData.model_validate(SAMPLE_CREATE_REQUEST)
        route = respx.post(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_CREATE_RESPONSE)
        )

        result = sync_client.proposal_attempts.create(PROPOSAL_ID, proposal_attempt)

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1


class TestProposalAttemptsList:
    @respx.mock
    def test_list_proposal_attempts(self, sync_client: CredereClient) -> None:
        route = respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_LIST_REPONSE)
        )

        result = sync_client.proposal_attempts.list(PROPOSAL_ID)

        assert route.called
        assert isinstance(result, list)
        assert isinstance(result[0], ProposalAttemptResponse)
        assert len(result) == 1
        assert result[0].id == 1


class TestProposalAttemptsGet:
    @respx.mock
    def test_get_proposal_attempt(self, sync_client: CredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_GET_RESPONSE)
        )

        result = sync_client.proposal_attempts.get(PROPOSAL_ID, 1)

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1


class TestProposalAttemptsUpdate:
    @respx.mock
    def test_update_proposal_attempt(self, sync_client: CredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1"
        proposal_attempt_updated = SAMPLE_PROPOSAL_ATTEMPT_RESPONSE.copy()
        proposal_attempt_updated["obs"] = "Updated observation"
        proposal_attemped_updated_cls = ProposalAttemptResponse(
            object_type=proposal_attempt_updated["object_type"],
            id=proposal_attempt_updated["id"],
            raw_response=proposal_attempt_updated,
        )
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=proposal_attempt_updated)
        )

        result = sync_client.proposal_attempts.update(
            PROPOSAL_ID, 1, proposal_attemped_updated_cls
        )

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1
        assert result.raw_response["obs"] == "Updated observation"


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


# ASYNC TESTS


class TestAsyncProposalAttemptsCreate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_create_proposal_attempt(
        self, async_client: AsyncCredereClient
    ) -> None:
        proposal_attempt = ProposalAttemptData.model_validate(SAMPLE_CREATE_REQUEST)
        route = respx.post(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_CREATE_RESPONSE)
        )

        result = await async_client.proposal_attempts.create(
            PROPOSAL_ID, proposal_attempt
        )

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1


class TestAsyncProposalAttemptsList:
    @respx.mock
    @pytest.mark.asyncio
    async def test_list_proposal_attempts(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_LIST_REPONSE)
        )

        result = await async_client.proposal_attempts.list(PROPOSAL_ID)

        assert route.called
        assert isinstance(result, list)
        assert isinstance(result[0], ProposalAttemptResponse)
        assert len(result) == 1
        assert result[0].id == 1


class TestAsyncProposalAttemptsGet:
    @respx.mock
    @pytest.mark.asyncio
    async def test_get_proposal_attempt(self, async_client: AsyncCredereClient) -> None:
        url = f"{ATTEMPTS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ATTEMPT_GET_RESPONSE)
        )

        result = await async_client.proposal_attempts.get(PROPOSAL_ID, "1")

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1


class TestAsyncProposalAttemptsUpdate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_update_proposal_attempt(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{ATTEMPTS_URL}/1"
        proposal_attempt_updated = SAMPLE_PROPOSAL_ATTEMPT_RESPONSE.copy()
        proposal_attempt_updated["obs"] = "Updated observation"
        proposal_attemped_updated_cls = ProposalAttemptResponse(
            object_type=proposal_attempt_updated["object_type"],
            id=proposal_attempt_updated["id"],
            raw_response=proposal_attempt_updated,
        )
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=proposal_attempt_updated)
        )

        result = await async_client.proposal_attempts.update(
            PROPOSAL_ID, "1", proposal_attemped_updated_cls
        )

        assert route.called
        assert isinstance(result, ProposalAttemptResponse)
        assert result.id == 1
        assert result.raw_response["obs"] == "Updated observation"


class TestAsyncErrorMapping:
    @respx.mock
    @pytest.mark.asyncio
    async def test_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(ATTEMPTS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await async_client.proposal_attempts.list(PROPOSAL_ID)

        assert exc_info.value.status_code == 401

    @respx.mock
    @pytest.mark.asyncio
    async def test_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
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
            await async_client.proposal_attempts.list(PROPOSAL_ID)

        assert exc_info.value.status_code == 404
