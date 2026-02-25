import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.proposals import (
    ProposalCreateRequest,
    ProposalCreateResponse,
    ProposalGetResponse,
    ProposalListResponse,
    ProposalUpdateRequest,
)

BASE_URL = "https://api.credere.com"
PROPOSALS_URL = f"{BASE_URL}/v1/proposals"

SAMPLE_PROPOSAL_CREATE_DATA = {
    "proposal": {
        "customer_id": 1,
        "store_id": 1,
        "seller_id": 1,
        "commercial": False,
        "proposal_attempts": [
            {
                "simulation_condition_id": 1,
                "external_simulation_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            }
        ],
    }
}

SAMPLE_PROPOSAL_CREATE_RESPONSE = {
    "object_type": "CdcProposal",
    "id": 1,
    "created_at": "2022-01-01T00:00:00.000-00:00",
    "updated_at": "2022-01-01T00:00:00.000-00:00",
    "customer": {
        "id": 1,
        "name": "Cliente 1",
        "cpf": "000.000.000-00",
        "cnpj": None,
        "born_at": "2000-01-01",
        "phones": [{"code": 84, "number": 987654321}],
    },
    "seller": {"id": 1, "name": "Nome do vendedor"},
    "state": "checagem",
    "store": {"id": 1, "name": "Credere", "seller_can_send_proposal_to_bank": True},
    "year_of_model": 2022,
    "year_of_manufacture": 2022,
    "comments_count": 0,
    "external_simulation_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "sent_to_bank": True,
    "zero_km": True,
    "commercial": False,
    "creation_external_link_id": None,
    "licensing_uf": "RN",
    "licensing_city": "Natal",
    "chassi_code": None,
    "license_plate_code": None,
    "renavam_code": None,
    "km_mileage": None,
    "color": None,
    "proposal_attempt": {
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
        "state_rank": 2,
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
    },
    "vehicle_model": {
        "object_type": "VehicleModel",
        "id": 1,
        "created_at": "2022-01-01T00:00:00.000-00:00",
        "updated_at": "2022-01-01T00:00:00.000-00:00",
        "name": "Biz",
        "brand": "Honda",
        "molicar_code": "00000000-0",
        "version": "110i CBS",
        "year_end": 2022,
        "year_start": 2022,
        "active": True,
        "public_price_cents": 1000000,
        "public_price_as_string": "BRL",
        "publish": False,
        "fipe_code": "000000-0",
        "public_picture": None,
        "vehicle_brand": {"id": 1, "name": "Honda"},
        "fuel": {
            "object_type": "Fuel",
            "id": 1,
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "name": "Gasolina",
        },
        "vehicle_type": {
            "id": 1,
            "name": "Motos",
            "created_at": "2022-01-01T00:00:00.000-00:00",
            "updated_at": "2022-01-01T00:00:00.000-00:00",
            "honda_code": "MOT",
        },
    },
    "fuel": {
        "object_type": "Fuel",
        "id": 1,
        "created_at": "2022-01-01T00:00:00.000-00:00",
        "updated_at": "2022-01-01T00:00:00.000-00:00",
        "name": "Gasolina",
    },
}

SAMPLE_PROPOSAL_GET_RESPONSE = {"proposal": SAMPLE_PROPOSAL_CREATE_RESPONSE}

SAMPLE_PROPOSALS_LIST_RESPONSE = {"proposals": [SAMPLE_PROPOSAL_CREATE_RESPONSE]}


class TestProposalsCreate:
    @respx.mock
    def test_create_proposal(self, sync_client: CredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_CREATE_RESPONSE)
        )

        proposal_create = ProposalCreateRequest.model_validate(
            SAMPLE_PROPOSAL_CREATE_DATA
        )
        proposal = sync_client.proposals.create(proposal_create)

        assert route.called
        assert isinstance(proposal, ProposalCreateResponse)
        assert proposal.id == 1
        assert (
            proposal.external_simulation_uuid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        )
        assert len(proposal.proposal_attempt.payment_flow) == 12


class TestProposalsList:
    @respx.mock
    def test_list_proposals(self, sync_client: CredereClient) -> None:
        route = respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_LIST_RESPONSE)
        )

        proposals = sync_client.proposals.list()

        assert route.called
        assert isinstance(proposals, ProposalListResponse)
        assert len(proposals.proposals) == 1
        assert isinstance(proposals.proposals[0], ProposalCreateResponse)
        assert proposals.proposals[0].id == 1


class TestProposalsGet:
    @respx.mock
    def test_get_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_GET_RESPONSE)
        )

        proposal = sync_client.proposals.get(proposal_id)

        assert route.called
        assert isinstance(proposal, ProposalGetResponse)
        assert proposal.proposal.id == 1


class TestProposalsUpdate:
    @respx.mock
    def test_update_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        new_proposal_data = SAMPLE_PROPOSAL_CREATE_DATA.copy()
        new_proposal_data["commercial"] = True
        new_proposal_data["id"] = proposal_id
        new_proposal_data_resp = SAMPLE_PROPOSAL_CREATE_RESPONSE.copy()
        new_proposal_data_resp["commercial"] = (
            True  # simulate the API response reflecting the update
        )
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=new_proposal_data_resp)
        )

        proposal_update = ProposalUpdateRequest.model_validate(new_proposal_data)
        proposal = sync_client.proposals.update(proposal_id, proposal_update)

        assert route.called
        assert isinstance(proposal, ProposalCreateResponse)
        assert proposal.id == 1
        assert proposal.commercial is True


class TestProposalsDelete:
    @respx.mock
    def test_delete_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = sync_client.proposals.delete(proposal_id)

        assert route.called
        assert result is None


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


# ASYNC TESTS


class TestAsyncProposalsCreate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_create_proposal(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_CREATE_RESPONSE)
        )

        proposal_create = ProposalCreateRequest.model_validate(
            SAMPLE_PROPOSAL_CREATE_DATA
        )
        # Added await
        proposal = await async_client.proposals.create(proposal_create)

        assert route.called
        assert isinstance(proposal, ProposalCreateResponse)
        assert proposal.id == 1
        assert (
            proposal.external_simulation_uuid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        )
        assert len(proposal.proposal_attempt.payment_flow) == 12


class TestAsyncProposalsList:
    @respx.mock
    @pytest.mark.asyncio
    async def test_list_proposals(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_LIST_RESPONSE)
        )

        # Added await
        proposals = await async_client.proposals.list()

        assert route.called
        assert isinstance(proposals, ProposalListResponse)
        assert len(proposals.proposals) == 1
        assert isinstance(proposals.proposals[0], ProposalCreateResponse)
        assert proposals.proposals[0].id == 1


class TestAsyncProposalsGet:
    @respx.mock
    @pytest.mark.asyncio
    async def test_get_proposal(self, async_client: AsyncCredereClient) -> None:
        proposal_id = "1"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_GET_RESPONSE)
        )

        # Added await
        proposal = await async_client.proposals.get(proposal_id)

        assert route.called
        assert isinstance(proposal, ProposalGetResponse)
        assert proposal.proposal.id == 1


class TestAsyncProposalsUpdate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_update_proposal(self, async_client: AsyncCredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        new_proposal_data = SAMPLE_PROPOSAL_CREATE_DATA.copy()
        new_proposal_data["commercial"] = True
        new_proposal_data["id"] = proposal_id

        new_proposal_data_resp = SAMPLE_PROPOSAL_CREATE_RESPONSE.copy()
        new_proposal_data_resp["commercial"] = True

        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=new_proposal_data_resp)
        )

        proposal_update = ProposalUpdateRequest.model_validate(new_proposal_data)
        # Added await
        proposal = await async_client.proposals.update(proposal_id, proposal_update)

        assert route.called
        assert isinstance(proposal, ProposalCreateResponse)
        assert proposal.id == 1
        assert proposal.commercial is True


class TestAsyncProposalsDelete:
    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_proposal(self, async_client: AsyncCredereClient) -> None:
        proposal_id = "1"
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        # Added await
        result = await async_client.proposals.delete(proposal_id)

        assert route.called
        assert result is None
