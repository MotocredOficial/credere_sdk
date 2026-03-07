import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.proposals import (
    ProposalData,
    ProposalResponse,
)

BASE_URL = "https://app.meucredere.com.br"
PROPOSALS_URL = f"{BASE_URL}/api/v1/proposals"

SAMPLE_PROPOSAL_CREATE_DATA = {
    "proposal": {
        "customer_id": 1,
        "store_id": 1,
        "seller_id": 1,
        "commercial": False,
        "proposal_attemps": [
            {
                "simulation_condition_id": 1,
                "external_simulation_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            }
        ],
    }
}

SAMPLE_PROPOSAL_CREATE_RESPONSE = {
    "complete_proposal": {
        "object_type": "CdcProposal",
        "id": 1,
        "created_at": "2022-03-04T15:02:23-03:00",
        "updated_at": "2022-03-04T15:02:23-03:00",
        "customer": {
            "id": 1,
            "name": "Cliente 1",
            "cpf": "615.211.390-32",
            "cnpj": None,
            "born_at": "1980-10-13",
            "phones": [{"code": 84, "number": 990000001}],
        },
        "seller": {"id": 2, "name": "Diretor"},
        "state": "checagem",
        "store": {"id": 1, "name": "Credere", "seller_can_send_proposal_to_bank": True},
        "year_of_model": 2021,
        "year_of_manufacture": 2021,
        "comments_count": 0,
        "external_simulation_uuid": "42c2e9f5-a422-4d45-b2ab-180694d63f3c",
        "sent_to_bank": False,
        "zero_km": True,
        "commercial": False,
        "creation_external_link_id": None,
        "licensing_uf": "RN",
        "chassi_code": None,
        "license_plate_code": None,
        "renavam_code": None,
        "km_mileage": None,
        "color": None,
        "proposal_attempt": {
            "object_type": "ProposalAttemp",
            "id": 1,
            "created_at": "2022-03-04T15:02:23-03:00",
            "updated_at": "2022-03-04T15:02:23-03:00",
            "active": True,
            "bank": {
                "id": 90,
                "name": "Banco Votorantim S.A.",
                "tradename": "Banco Votorantim",
                "febraban_code": "655",
            },
            "input_financing_in_cents": 400000,
            "plan": {"return": "0.0"},
            "quota_in_cents": 55712,
            "state": "checagem",
            "table": {"description": "BVMIY - motos"},
            "term_financing": 12,
            "value_in_cents": 900000,
            "obs": None,
            "value_of_the_license_plate_in_cents": 50000,
            "financed_amount_in_cents": 589479,
            "coefficient": None,
            "has_license_plate": True,
            "first_payment_in_days": 30,
            "funding_type": {"id": 1, "name": "CDC"},
            "payment_type": {"id": 1, "name": "Carnê"},
            "input_origin": 1,
            "application": {"id": 1, "name": "Grupo X"},
            "external_simulation_uuid": "42c2e9f5-a422-4d45-b2ab-180694d63f3c",
            "simulation_condition_id": 19,
            "external_proposal_uuid": None,
            "integration_error": None,
            "state_rank": 6,
            "bank_proposal_identifier": None,
            "honda_id": None,
            "simulation_pre_approval_status": 2,
            "fixed_installments": True,
            "cet_monthly": None,
            "cet_annually": None,
            "replaced_by_proposal_attempt_id": None,
            "return_value_cents": None,
            "formalization_state": None,
            "formalization": None,
            "expenses": [
                {
                    "object_type": "ExpenseInfo",
                    "id": 2,
                    "created_at": "2022-03-04T15:02:23-03:00",
                    "updated_at": "2022-03-04T15:02:23-03:00",
                    "value_in_cents": 32579,
                    "credere_type": "spf",
                    "description": None,
                    "expense": None,
                },
                {
                    "object_type": "ExpenseInfo",
                    "id": 1,
                    "created_at": "2022-03-04T15:02:23-03:00",
                    "updated_at": "2022-03-04T15:02:23-03:00",
                    "value_in_cents": 56900,
                    "credere_type": "contract_record_rate",
                    "description": None,
                    "expense": None,
                },
            ],
            "payment_flow": [
                {"installment_number": 12, "value_cents": 55712},
                {"installment_number": 11, "value_cents": 55712},
                {"installment_number": 10, "value_cents": 55712},
                {"installment_number": 9, "value_cents": 55712},
                {"installment_number": 8, "value_cents": 55712},
                {"installment_number": 7, "value_cents": 55712},
                {"installment_number": 6, "value_cents": 55712},
                {"installment_number": 5, "value_cents": 55712},
                {"installment_number": 4, "value_cents": 55712},
                {"installment_number": 3, "value_cents": 55712},
                {"installment_number": 2, "value_cents": 55712},
                {"installment_number": 1, "value_cents": 55712},
            ],
        },
        "vehicle_model": {
            "object_type": "VehicleModel",
            "id": 1,
            "created_at": "2022-03-03T08:25:49-03:00",
            "updated_at": "2022-03-03T11:16:37-03:00",
            "name": "Biz",
            "brand": "Honda",
            "molicar_code": "01906112-2",
            "version": "110i CBS",
            "year_end": 2021,
            "year_start": 2020,
            "active": True,
            "public_price_cents": 900000,
            "public_price_as_string": None,
            "publish": False,
            "fipe_code": "811138-3",
            "public_picture": None,
            "vehicle_brand": {"id": 1, "name": "Honda"},
            "fuel": {
                "object_type": "Fuel",
                "id": 1,
                "created_at": "2022-03-03T08:22:28-03:00",
                "updated_at": "2022-03-03T08:22:28-03:00",
                "name": "Gasolina",
            },
            "vehicle_type": {
                "created_at": "2022-03-03T08:22:16-03:00",
                "honda_code": "MOT",
                "id": 3,
                "name": "Motos",
                "updated_at": "2022-03-03T08:22:16-03:00",
            },
        },
        "fuel": {
            "object_type": "Fuel",
            "id": 1,
            "created_at": "2022-03-03T08:22:28-03:00",
            "updated_at": "2022-03-03T08:22:28-03:00",
            "name": "Gasolina",
        },
    }
}

SAMPLE_PROPOSAL_GET_RESPONSE = {
    "proposal": SAMPLE_PROPOSAL_CREATE_RESPONSE["complete_proposal"]
}

SAMPLE_PROPOSALS_LIST_RESPONSE = {
    "proposals": [SAMPLE_PROPOSAL_CREATE_RESPONSE["complete_proposal"]]
}


class TestProposalsCreate:
    @respx.mock
    def test_create_proposal(self, sync_client: CredereClient) -> None:
        route = respx.post(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSAL_CREATE_RESPONSE)
        )

        proposal_create = ProposalData.model_validate(
            SAMPLE_PROPOSAL_CREATE_DATA["proposal"]
        )
        proposal = sync_client.proposals.create(proposal_create)

        assert route.called
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1
        assert (
            proposal.raw_response["external_simulation_uuid"]
            == "42c2e9f5-a422-4d45-b2ab-180694d63f3c"
        )
        assert len(proposal.raw_response["proposal_attempt"]["payment_flow"]) == 12


class TestProposalsList:
    @respx.mock
    def test_list_proposals(self, sync_client: CredereClient) -> None:
        route = respx.get(PROPOSALS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_PROPOSALS_LIST_RESPONSE)
        )

        proposals = sync_client.proposals.list()

        assert route.called
        assert isinstance(proposals, list)
        assert len(proposals) == 1
        assert isinstance(proposals[0], ProposalResponse)
        assert proposals[0].id == 1


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
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1


class TestProposalsUpdate:
    @respx.mock
    def test_update_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        new_proposal_data = SAMPLE_PROPOSAL_CREATE_DATA["proposal"].copy()
        new_proposal_data["commercial"] = True
        new_proposal_data_resp = SAMPLE_PROPOSAL_CREATE_RESPONSE[
            "complete_proposal"
        ].copy()
        new_proposal_data_resp["commercial"] = (
            True  # simulate response reflecting the update
        )
        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=new_proposal_data_resp)
        )

        proposal_update = ProposalData.model_validate(new_proposal_data)
        proposal = sync_client.proposals.update(proposal_id, proposal_update)

        assert route.called
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1
        assert proposal.raw_response["commercial"] is True


class TestProposalsDelete:
    @respx.mock
    def test_delete_proposal(self, sync_client: CredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = sync_client.proposals.delete(proposal_id)

        assert route.called
        assert result is None


class TestProposalsActivityLog:
    @respx.mock
    def test_activity_log(self, sync_client: CredereClient) -> None:
        proposal_id = "1"
        url = f"{PROPOSALS_URL}/{proposal_id}/activity_log"
        log_data = {
            "activities": [
                {"id": 1, "action": "created", "created_at": "2022-03-04"},
                {"id": 2, "action": "updated", "created_at": "2022-03-05"},
            ]
        }
        route = respx.get(url).mock(return_value=httpx.Response(200, json=log_data))

        result = sync_client.proposals.activity_log(proposal_id)

        assert route.called
        assert result == log_data
        assert len(result["activities"]) == 2
        assert result["activities"][0]["action"] == "created"


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

        proposal_create = ProposalData.model_validate(
            SAMPLE_PROPOSAL_CREATE_DATA["proposal"]
        )
        # Added await
        proposal = await async_client.proposals.create(proposal_create)

        assert route.called
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1
        assert (
            proposal.raw_response["external_simulation_uuid"]
            == "42c2e9f5-a422-4d45-b2ab-180694d63f3c"
        )
        assert len(proposal.raw_response["proposal_attempt"]["payment_flow"]) == 12


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
        assert isinstance(proposals, list)
        assert len(proposals) == 1
        assert isinstance(proposals[0], ProposalResponse)
        assert proposals[0].id == 1


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
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1


class TestAsyncProposalsUpdate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_update_proposal(self, async_client: AsyncCredereClient) -> None:
        proposal_id = 1
        url = f"{PROPOSALS_URL}/{proposal_id}"
        new_proposal_data = SAMPLE_PROPOSAL_CREATE_DATA["proposal"].copy()
        new_proposal_data["commercial"] = True

        new_proposal_data_resp = SAMPLE_PROPOSAL_CREATE_RESPONSE[
            "complete_proposal"
        ].copy()
        new_proposal_data_resp["commercial"] = True

        route = respx.put(url).mock(
            return_value=httpx.Response(200, json=new_proposal_data_resp)
        )

        proposal_update = ProposalData.model_validate(new_proposal_data)
        # Added await
        proposal = await async_client.proposals.update(proposal_id, proposal_update)

        assert route.called
        assert isinstance(proposal, ProposalResponse)
        assert proposal.id == 1
        assert proposal.raw_response["commercial"] is True


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


class TestAsyncProposalsActivityLog:
    @respx.mock
    @pytest.mark.asyncio
    async def test_async_activity_log(self, async_client: AsyncCredereClient) -> None:
        proposal_id = "1"
        url = f"{PROPOSALS_URL}/{proposal_id}/activity_log"
        log_data = {
            "activities": [
                {"id": 1, "action": "created", "created_at": "2022-03-04"},
            ]
        }
        route = respx.get(url).mock(return_value=httpx.Response(200, json=log_data))

        result = await async_client.proposals.activity_log(proposal_id)

        assert route.called
        assert result == log_data
        assert result["activities"][0]["action"] == "created"
