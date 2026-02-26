"""Tests for the Leads resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, CredereAPIError, NotFoundError
from credere.models.leads import LeadData, LeadRequiredFields, LeadResponse

BASE_URL = "https://api.credere.com"
LEADS_URL = f"{BASE_URL}/v1/banks_api/leads"

SAMPLE_LEAD_CREATE_DATA = {
    "lead": {
        "address": {
            "city": "Natal",
            "complement": "Edif Corporate Tower Edif Center-Trade",
            "district": "Lagoa Nova",
            "number": "3700, Sala 409 Bloco A",
            "state": "RN",
            "street": "Av Amintas Barros",
            "zip_code": "59075-810",
        },
        "cpf_cnpj": "000.000.000-00",
        "name": "Client name",
        "birthdate": "1970-01-01",
        "phone_number": "(84) 90000-0000",
        "email": "cliente@email.com",
        "retrieve_gender": "F",
        "retrieve_occupation": "11",
        "retrieve_profession": "administrador",
        "monthly_income": 900000,
        "has_cnh": True,
    }
}

SAMPLE_LEAD_RESPONSE = {
    "data": {
        "id": 1,
        "cpf_cnpj": "597.352.160-51",
        "name": "Lead Name",
        "gender": {
            "id": 1,
            "type": "domain_type",
            "credere_identifier": "credere_identifier",
            "label": "Domain Label",
        },
        "occupation": {
            "id": 1,
            "type": "domain_type",
            "credere_identifier": "credere_identifier",
            "label": "Domain Label",
        },
        "profession": {
            "id": 1,
            "type": "domain_type",
            "credere_identifier": "credere_identifier",
            "label": "Domain Label",
        },
        "birthdate": "1995-11-24",
        "monthly_income": 1500000,
        "phone_number": "+5582999001000",
        "payload": {},
        "address": {
            "id": 1,
            "zip_code": "59075810",
            "street": "Av Amintas Barros",
            "number": "3700, Sala 409 Bloco A",
            "complement": "Edif Corporate Tower Edif Center-Trade",
            "city": "Natal",
            "state": "RN",
        },
    }
}

SAMPLE_LEAD_REQUIRED_FIELDS_RESPONSE = {
    "data": {
        "lead": {
            "id": 1,
            "cpf_cnpj": "597.352.160-51",
            "name": "Lead Name",
            "gender": {
                "id": 1,
                "type": "domain_type",
                "credere_identifier": "credere_identifier",
                "label": "Domain Label",
            },
            "occupation": {
                "id": 1,
                "type": "domain_type",
                "credere_identifier": "credere_identifier",
                "label": "Domain Label",
            },
            "profession": {
                "id": 1,
                "type": "domain_type",
                "credere_identifier": "credere_identifier",
                "label": "Domain Label",
            },
            "birthdate": "1995-11-24",
            "mother_name": "Lead Mother Name",
            "monthly_income": 1500000,
            "phone_number": "+5582999001000",
            "payload": {},
            "address": {
                "id": 1,
                "zip_code": "59075810",
                "street": "Av Amintas Barros",
                "number": "3700, Sala 409 Bloco A",
                "complement": "Edif Corporate Tower Edif Center-Trade",
                "city": "Natal",
                "state": "RN",
            },
        },
        "requirements": {
            "address": {"zip_code": ["623"]},
            "birthdate": ["fontecred", "655", "623", "394", "336"],
            "cpf_cnpj": [
                "moneyplus",
                "fontecred",
                "M22",
                "655",
                "623",
                "422",
                "394",
                "342",
                "341",
                "336",
            ],
            "has_cnh": ["341", "336"],
            "monthly_income": ["623"],
            "name": ["fontecred", "422", "394"],
            "phone_number": ["fontecred", "655", "623", "336"],
            "retrieve_gender": ["394"],
            "retrieve_occupation": ["623"],
        },
    }
}

SAMPLE_LEAD_LIST_RESPONSE = {"data": [SAMPLE_LEAD_RESPONSE["data"]]}


class TestLeadsCreate:
    @respx.mock
    def test_create_lead(self, sync_client: CredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead_data = LeadData.model_validate(SAMPLE_LEAD_CREATE_DATA["lead"])
        lead = sync_client.leads.create(lead_data)

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1
        assert lead.cpf_cnpj == "597.352.160-51"
        assert lead.name == "Lead Name"
        assert lead.gender is not None
        assert lead.gender.credere_identifier == "credere_identifier"
        assert lead.address is not None
        assert lead.address.id == 1


class TestLeadsUpdate:
    @respx.mock
    def test_update_lead(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        updated_data = SAMPLE_LEAD_RESPONSE["data"].copy()
        updated_data["name"] = "João Atualizado"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json={"data": updated_data})
        )

        lead_data = LeadData.model_validate(SAMPLE_LEAD_CREATE_DATA["lead"])
        lead_data.name = "João Atualizado"

        lead = sync_client.leads.update("12345678900", lead_data)

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1


class TestLeadsDelete:
    @respx.mock
    def test_delete_lead(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = sync_client.leads.delete("12345678900")

        assert route.called
        assert result is None


class TestLeadsList:
    @respx.mock
    def test_list_leads(self, sync_client: CredereClient) -> None:
        route = respx.get(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_LIST_RESPONSE)
        )

        leads = sync_client.leads.list()

        assert route.called
        assert isinstance(leads, list)
        assert len(leads) == 1
        assert isinstance(leads[0], LeadResponse)
        assert leads[0].cpf_cnpj == "597.352.160-51"


class TestLeadsGet:
    @respx.mock
    def test_get_lead(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/59732516051"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = sync_client.leads.get("59732516051")

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1


class TestLeadsRequiredFields:
    @respx.mock
    def test_required_fields(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900/required_fields"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_REQUIRED_FIELDS_RESPONSE)
        )

        result = sync_client.leads.required_fields("12345678900")

        assert route.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None
        assert result.lead.id == 1
        assert result.requirements is not None
        assert "birthdate" in result.requirements


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(LEADS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.leads.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/00000000000"
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
            sync_client.leads.get("00000000000")

        assert exc_info.value.status_code == 404

    @respx.mock
    def test_422_raises_credere_api_error(self, sync_client: CredereClient) -> None:
        respx.post(LEADS_URL).mock(
            return_value=httpx.Response(
                422,
                json={"error": {"message": "Invalid CPF/CNPJ", "status": 422}},
            )
        )

        with pytest.raises(CredereAPIError) as exc_info:
            sync_client.leads.create(LeadData(cpf_cnpj="invalid"))

        assert exc_info.value.status_code == 422

    @respx.mock
    def test_500_raises_credere_api_error(self, sync_client: CredereClient) -> None:
        respx.get(LEADS_URL).mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        with pytest.raises(CredereAPIError) as exc_info:
            sync_client.leads.list()

        assert exc_info.value.status_code == 500


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncLeadsCreate:
    @respx.mock
    async def test_async_create_lead(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead_data = LeadData.model_validate(SAMPLE_LEAD_CREATE_DATA["lead"])
        lead = await async_client.leads.create(lead_data)

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1
        assert lead.cpf_cnpj == "597.352.160-51"
        assert lead.name == "Lead Name"
        assert lead.gender is not None
        assert lead.gender.credere_identifier == "credere_identifier"
        assert lead.address is not None
        assert lead.address.id == 1


class TestAsyncLeadsUpdate:
    @respx.mock
    async def test_async_update_lead(self, async_client: AsyncCredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        updated_data = SAMPLE_LEAD_RESPONSE["data"].copy()
        updated_data["name"] = "João Atualizado"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json={"data": updated_data})
        )

        lead_data = LeadData.model_validate(SAMPLE_LEAD_CREATE_DATA["lead"])
        lead_data.name = "João Atualizado"

        lead = await async_client.leads.update("12345678900", lead_data)

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1


class TestAsyncLeadsDelete:
    @respx.mock
    async def test_async_delete_lead(self, async_client: AsyncCredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = await async_client.leads.delete("12345678900")

        assert route.called
        assert result is None


class TestAsyncLeadsList:
    @respx.mock
    async def test_async_list_leads(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_LIST_RESPONSE)
        )

        leads = await async_client.leads.list()

        assert route.called
        assert isinstance(leads, list)
        assert len(leads) == 1
        assert isinstance(leads[0], LeadResponse)
        assert leads[0].cpf_cnpj == "597.352.160-51"


class TestAsyncLeadsGet:
    @respx.mock
    async def test_async_get_lead(self, async_client: AsyncCredereClient) -> None:
        url = f"{LEADS_URL}/59732516051"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = await async_client.leads.get("59732516051")

        assert route.called
        assert isinstance(lead, LeadResponse)
        assert lead.id == 1


class TestAsyncLeadsRequiredFields:
    @respx.mock
    async def test_async_required_fields(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{LEADS_URL}/12345678900/required_fields"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_REQUIRED_FIELDS_RESPONSE)
        )

        result = await async_client.leads.required_fields("12345678900")

        assert route.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None
        assert result.lead.id == 1
        assert result.requirements is not None
        assert "birthdate" in result.requirements
