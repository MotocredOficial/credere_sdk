"""Tests for the Leads resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, CredereAPIError, NotFoundError
from credere.models.leads import Lead, LeadCreateRequest, LeadRequiredFields

BASE_URL = "https://api.credere.com"
LEADS_URL = f"{BASE_URL}/v1/banks_api/leads"

SAMPLE_LEAD_RESPONSE = {
    "data": {
        "id": 1,
        "cpf_cnpj": "12345678900",
        "name": "João Silva",
        "birthdate": "1990-01-15",
        "monthly_income": 500000,
        "phone_number": "11999999999",
        "payload": {},
        "gender": {
            "id": 1,
            "type": "Gender",
            "credere_identifier": "male",
            "label": "Masculino",
        },
        "occupation": {
            "id": 10,
            "type": "Occupation",
            "credere_identifier": "employee",
            "label": "Empregado",
        },
        "profession": {
            "id": 20,
            "type": "Profession",
            "credere_identifier": "engineer",
            "label": "Engenheiro",
        },
        "mother_name": "Maria Silva",
        "address": {
            "id": 100,
            "zip_code": "01001000",
            "street": "Rua Direita",
            "number": "123",
            "complement": "Apto 1",
            "district": "Sé",
            "city": "São Paulo",
            "state": "SP",
        },
    }
}

SAMPLE_LIST_RESPONSE = {"data": [SAMPLE_LEAD_RESPONSE["data"]]}

SAMPLE_REQUIRED_FIELDS_RESPONSE = {
    "data": {
        "lead": SAMPLE_LEAD_RESPONSE["data"],
        "requirements": {
            "birthdate": ["bank_code_1"],
            "cpf_cnpj": ["bank_code_1"],
            "name": ["bank_code_1"],
            "phone_number": ["bank_code_1"],
            "address": {"zip_code": ["bank_code_1"]},
        },
    }
}

SAMPLE_CREATE_DATA = LeadCreateRequest(
    cpf_cnpj="12345678900",
    name="João Silva",
    birthdate="1990-01-15",
    email="joao@example.com",
    has_cnh=True,
    retrieve_gender="male",
    phone_number="11999999999",
    monthly_income=500000,
)


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestLeadsCreate:
    @respx.mock
    def test_create_lead(self, sync_client: CredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = sync_client.leads.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(lead, Lead)
        assert lead.id == 1
        assert lead.cpf_cnpj == "12345678900"
        assert lead.name == "João Silva"
        assert lead.gender is not None
        assert lead.gender.credere_identifier == "male"
        assert lead.address is not None
        assert lead.address.id == 100

    @respx.mock
    def test_create_sends_correct_body(self, sync_client: CredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        sync_client.leads.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"
        assert "Authorization" in request.headers

    @respx.mock
    def test_create_sends_json_body(self, sync_client: CredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        sync_client.leads.create(SAMPLE_CREATE_DATA)

        import json

        body = json.loads(route.calls.last.request.content)
        assert "lead" in body
        assert body["lead"]["cpf_cnpj"] == "12345678900"


class TestLeadsUpdate:
    @respx.mock
    def test_update_lead(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        update_data = LeadCreateRequest(name="João Atualizado")
        lead = sync_client.leads.update("12345678900", update_data)

        assert route.called
        assert isinstance(lead, Lead)
        assert lead.id == 1

    @respx.mock
    def test_update_sends_correct_path_and_headers(
        self, sync_client: CredereClient
    ) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        sync_client.leads.update("12345678900", LeadCreateRequest(name="Test"))

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"


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
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        leads = sync_client.leads.list()

        assert route.called
        assert isinstance(leads, list)
        assert len(leads) == 1
        assert isinstance(leads[0], Lead)
        assert leads[0].cpf_cnpj == "12345678900"


class TestLeadsGet:
    @respx.mock
    def test_get_lead(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = sync_client.leads.get("12345678900")

        assert route.called
        assert isinstance(lead, Lead)
        assert lead.id == 1
        assert lead.mother_name == "Maria Silva"


class TestLeadsRequiredFields:
    @respx.mock
    def test_required_fields(self, sync_client: CredereClient) -> None:
        url = f"{LEADS_URL}/12345678900/required_fields"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_REQUIRED_FIELDS_RESPONSE)
        )

        result = sync_client.leads.required_fields("12345678900")

        assert route.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None
        assert result.lead.id == 1
        assert result.requirements is not None
        assert "birthdate" in result.requirements


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


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
            sync_client.leads.create(LeadCreateRequest(cpf_cnpj="invalid"))

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
# Store-Id override tests
# ---------------------------------------------------------------------------


class TestStoreIdOverride:
    @respx.mock
    def test_method_store_id_overrides_client(self, sync_client: CredereClient) -> None:
        route = respx.get(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        sync_client.leads.list(store_id=99)

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "99"

    @respx.mock
    def test_no_store_id_omits_header(self) -> None:
        client = CredereClient(api_key="sk-test", base_url=BASE_URL)
        route = respx.get(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        client.leads.list()

        request = route.calls.last.request
        assert "Store-Id" not in request.headers
        client.close()


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncLeadsCreate:
    @respx.mock
    async def test_async_create_lead(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = await async_client.leads.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(lead, Lead)
        assert lead.id == 1
        assert lead.cpf_cnpj == "12345678900"


class TestAsyncLeadsList:
    @respx.mock
    async def test_async_list_leads(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(LEADS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        leads = await async_client.leads.list()

        assert route.called
        assert len(leads) == 1
        assert isinstance(leads[0], Lead)


class TestAsyncLeadsGet:
    @respx.mock
    async def test_async_get_lead(self, async_client: AsyncCredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_LEAD_RESPONSE)
        )

        lead = await async_client.leads.get("12345678900")

        assert route.called
        assert isinstance(lead, Lead)
        assert lead.id == 1


class TestAsyncLeadsDelete:
    @respx.mock
    async def test_async_delete_lead(self, async_client: AsyncCredereClient) -> None:
        url = f"{LEADS_URL}/12345678900"
        route = respx.delete(url).mock(return_value=httpx.Response(204))

        result = await async_client.leads.delete("12345678900")

        assert route.called
        assert result is None


class TestAsyncLeadsRequiredFields:
    @respx.mock
    async def test_async_required_fields(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{LEADS_URL}/12345678900/required_fields"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_REQUIRED_FIELDS_RESPONSE)
        )

        result = await async_client.leads.required_fields("12345678900")

        assert route.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None


class TestAsyncErrorMapping:
    @respx.mock
    async def test_async_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(LEADS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError):
            await async_client.leads.list()

    @respx.mock
    async def test_async_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{LEADS_URL}/00000000000"
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
            await async_client.leads.get("00000000000")
