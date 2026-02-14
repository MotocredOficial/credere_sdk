"""Tests for the Proposals resource (sync + async)."""

import json

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.proposals import (
    Proposal,
    ProposalConditionRequest,
    ProposalCreateRequest,
    ProposalVehicleRequest,
)

BASE_URL = "https://api.credere.com"
PROPOSALS_URL = f"{BASE_URL}/v1/proposals"

SAMPLE_CONDITION = {
    "installments": 48,
    "down_payment": 1000000,
    "financed_amount": 4000000,
    "bank": {
        "id": 10,
        "febraban_code": "341",
        "name": "Itaú Unibanco",
        "nickname": "Itaú",
    },
    "interest_monthly": 1.49,
    "cet_monthly": 1.62,
    "cet_annually": 21.28,
}

SAMPLE_VEHICLE = {
    "asset_value": 5000000,
    "licensing_uf": "SP",
    "manufacture_year": 2024,
    "model_year": 2024,
    "vehicle_molicar_code": "MOL123",
    "zero_km": True,
}

SAMPLE_PROPOSAL_RESPONSE = {
    "data": {
        "id": "prop-abc-123",
        "assets_value": 5000000,
        "documentation_value": 50000,
        "conditions": [SAMPLE_CONDITION],
        "vehicle": SAMPLE_VEHICLE,
        "retrieve_lead": {"cpf_cnpj": "12345678900"},
        "seller_cpf": "98765432100",
        "status": "pending",
        "created_at": "2024-01-15T10:00:00-03:00",
        "updated_at": "2024-01-15T10:00:00-03:00",
    }
}

SAMPLE_LIST_RESPONSE = {"data": [SAMPLE_PROPOSAL_RESPONSE["data"]]}

SAMPLE_ACTIVITY_LOG_RESPONSE = {
    "data": [
        {"action": "created", "user": "john", "timestamp": "2024-01-15T10:00:00-03:00"},
        {"action": "updated", "user": "jane", "timestamp": "2024-01-15T11:00:00-03:00"},
    ]
}

SAMPLE_CREATE_DATA = ProposalCreateRequest(
    assets_value=5000000,
    documentation_value=50000,
    conditions=[
        ProposalConditionRequest(
            down_payment=1000000,
            financed_amount=4000000,
            installments=48,
        )
    ],
    retrieve_lead={"cpf_cnpj": "12345678900"},
    seller_cpf="98765432100",
    vehicle=ProposalVehicleRequest(
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


class TestProposalsCreate:
    @respx.mock
    def test_create_proposal(self, sync_client: CredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = sync_client.proposals.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"
        assert proposal.assets_value == 5000000
        assert proposal.status == "pending"
        assert proposal.conditions is not None
        assert len(proposal.conditions) == 1
        assert proposal.conditions[0].bank is not None
        assert proposal.conditions[0].bank.febraban_code == "341"
        assert proposal.vehicle is not None
        assert proposal.vehicle.zero_km is True

    @respx.mock
    def test_create_sends_correct_body(self, sync_client: CredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        sync_client.proposals.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        body = json.loads(request.content)
        assert "proposal" in body
        assert body["proposal"]["assets_value"] == 5000000
        assert body["proposal"]["seller_cpf"] == "98765432100"
        assert body["proposal"]["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(body["proposal"]["conditions"]) == 1
        assert body["proposal"]["vehicle"]["zero_km"] is True

    @respx.mock
    def test_create_sends_store_id_header(self, sync_client: CredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        sync_client.proposals.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"


class TestProposalsList:
    @respx.mock
    def test_list_proposals(self, sync_client: CredereClient) -> None:
        route = respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        proposals = sync_client.proposals.list()

        assert route.called
        assert isinstance(proposals, list)
        assert len(proposals) == 1
        assert isinstance(proposals[0], Proposal)
        assert proposals[0].id == "prop-abc-123"


class TestProposalsGet:
    @respx.mock
    def test_get_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = sync_client.proposals.get(proposal_id)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"
        assert proposal.conditions is not None
        assert proposal.conditions[0].interest_monthly == 1.49


class TestProposalsUpdate:
    @respx.mock
    def test_update_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = sync_client.proposals.update(proposal_id, SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"

    @respx.mock
    def test_update_sends_correct_body(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        sync_client.proposals.update(proposal_id, SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        body = json.loads(request.content)
        assert "proposal" in body
        assert body["proposal"]["assets_value"] == 5000000


class TestProposalsDelete:
    @respx.mock
    def test_delete_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = sync_client.proposals.delete(proposal_id)

        assert route.called
        assert result is None


class TestProposalsGetOwnership:
    @respx.mock
    def test_get_ownership(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}/get_ownership"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = sync_client.proposals.get_ownership(proposal_id)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"


class TestProposalsLeaveOwnership:
    @respx.mock
    def test_leave_ownership(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}/leave_ownership"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = sync_client.proposals.leave_ownership(proposal_id)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"


class TestProposalsActivityLog:
    @respx.mock
    def test_activity_log(self, sync_client: CredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}/activity_log"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_ACTIVITY_LOG_RESPONSE)
        )

        log = sync_client.proposals.activity_log(proposal_id)

        assert route.called
        assert isinstance(log, list)
        assert len(log) == 2
        assert log[0]["action"] == "created"
        assert log[1]["action"] == "updated"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestProposalsErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.proposals.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{PROPOSALS_URL}/nonexistent"
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
            sync_client.proposals.get("nonexistent")

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncProposalsCreate:
    @respx.mock
    async def test_async_create_proposal(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = await async_client.proposals.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"
        assert proposal.conditions is not None
        assert len(proposal.conditions) == 1


class TestAsyncProposalsList:
    @respx.mock
    async def test_async_list_proposals(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        proposals = await async_client.proposals.list()

        assert route.called
        assert len(proposals) == 1
        assert isinstance(proposals[0], Proposal)


class TestAsyncProposalsGet:
    @respx.mock
    async def test_async_get_proposal(self, async_client: AsyncCredereClient) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_RESPONSE)
        )

        proposal = await async_client.proposals.get(proposal_id)

        assert route.called
        assert isinstance(proposal, Proposal)
        assert proposal.id == "prop-abc-123"


class TestAsyncProposalsDelete:
    @respx.mock
    async def test_async_delete_proposal(
        self, async_client: AsyncCredereClient
    ) -> None:
        proposal_id = "prop-abc-123"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = await async_client.proposals.delete(proposal_id)

        assert route.called
        assert result is None


class TestAsyncProposalsErrorMapping:
    @respx.mock
    async def test_async_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError):
            await async_client.proposals.list()

    @respx.mock
    async def test_async_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{PROPOSALS_URL}/nonexistent"
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
            await async_client.proposals.get("nonexistent")
