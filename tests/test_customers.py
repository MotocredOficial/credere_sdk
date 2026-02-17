"""Tests for the Customers resource (sync + async)."""

import json

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.customers import Customer, CustomerCreateRequest

BASE_URL = "https://api.credere.com"
CUSTOMERS_URL = f"{BASE_URL}/v1/customers"

SAMPLE_CUSTOMER_RESPONSE = {
    "customer": {
        "id": 1,
        "object_type": "Customer",
        "cpf_cnpj": "12345678901",
        "name": "Maria Souza",
        "email": "maria@example.com",
        "birthdate": "1985-05-20",
        "phone_number": "11988887777",
        "gender": {
            "id": 2,
            "type": "Gender",
            "credere_identifier": "female",
            "label": "Feminino",
        },
        "profession": {
            "id": 30,
            "type": "Profession",
            "credere_identifier": "lawyer",
            "label": "Advogado",
        },
        "occupation": {
            "id": 15,
            "type": "Occupation",
            "credere_identifier": "self_employed",
            "label": "Autônomo",
        },
        "monthly_income": 800000,
        "mother_name": "Ana Souza",
        "address": {
            "id": 200,
            "zip_code": "04001000",
            "street": "Av. Paulista",
            "number": "1000",
            "complement": "Sala 101",
            "district": "Bela Vista",
            "city": "São Paulo",
            "state": "SP",
        },
        "active": True,
        "created_at": "2024-06-01T10:00:00-03:00",
        "updated_at": "2024-06-01T10:00:00-03:00",
    }
}

SAMPLE_LIST_RESPONSE = {"customers": [SAMPLE_CUSTOMER_RESPONSE["customer"]]}

SAMPLE_CREATE_DATA = CustomerCreateRequest(
    cpf_cnpj="12345678901",
    name="Maria Souza",
    email="maria@example.com",
    birthdate="1985-05-20",
    phone_number="11988887777",
    monthly_income=800000,
)


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestCustomersCreate:
    @respx.mock
    def test_create_customer(self, sync_client: CredereClient) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = sync_client.customers.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"
        assert customer.name == "Maria Souza"
        assert customer.email == "maria@example.com"
        assert customer.active is True
        assert customer.address is not None
        assert customer.address.id == 200

    @respx.mock
    def test_create_sends_correct_body(self, sync_client: CredereClient) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        sync_client.customers.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        body = json.loads(request.content)
        assert "customer" in body
        assert body["customer"]["cpf_cnpj"] == "12345678901"
        assert body["customer"]["name"] == "Maria Souza"

    @respx.mock
    def test_create_sends_store_id_header(self, sync_client: CredereClient) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        sync_client.customers.create(SAMPLE_CREATE_DATA)

        request = route.calls.last.request
        assert request.headers["Store-Id"] == "42"


class TestCustomersUpdate:
    @respx.mock
    def test_update_customer(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        update_data = CustomerCreateRequest(name="Maria Atualizada")
        customer = sync_client.customers.update(1, update_data)

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1

    @respx.mock
    def test_update_sends_correct_body(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        sync_client.customers.update(1, CustomerCreateRequest(name="Maria Atualizada"))

        request = route.calls.last.request
        body = json.loads(request.content)
        assert "customer" in body
        assert body["customer"]["name"] == "Maria Atualizada"


class TestCustomersList:
    @respx.mock
    def test_list_customers(self, sync_client: CredereClient) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        customers = sync_client.customers.list()

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)
        assert customers[0].cpf_cnpj == "12345678901"

    @respx.mock
    def test_list_customers_with_params(self, sync_client: CredereClient) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        customers = sync_client.customers.list(
            page=1, cpf_cnpj="12345678901", name="Maria"
        )

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)
        assert customers[0].cpf_cnpj == "12345678901"

    @respx.mock
    def test_list_customers_with_inexisting_cpf(
        self, sync_client: CredereClient
    ) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json={"customers": []})
        )

        customers = sync_client.customers.list(
            cpf_cnpj="00000000000",
        )

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 0


class TestCustomersGet:
    @respx.mock
    def test_get_customer(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = sync_client.customers.get(1)

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.mother_name == "Ana Souza"


class TestCustomersFind:
    @respx.mock
    def test_find_customer(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = sync_client.customers.find(cpf_cnpj="12345678901")

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"

    @respx.mock
    def test_find_customer_with_params(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = sync_client.customers.find(cpf_cnpj="12345678901")

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"

    @respx.mock
    def test_find_customer_with_inexisting_cpf(
        self, sync_client: CredereClient
    ) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(
                404,
                json={
                    "error": {
                        "message": "Couldn't find Customer",
                        "class": "ActiveRecord::RecordNotFound",
                        "status": 404,
                    }
                },
            )
        )

        with pytest.raises(NotFoundError) as exc:
            sync_client.customers.find(cpf="00000000000")

        assert route.called
        assert exc.value.status_code == 404


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.customers.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/99999"
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
            sync_client.customers.get(99999)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncCustomersCreate:
    @respx.mock
    async def test_async_create_customer(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.create(SAMPLE_CREATE_DATA)

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"


class TestAsyncCustomersList:
    @respx.mock
    async def test_async_list_customers(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        customers = await async_client.customers.list()

        assert route.called
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)

    @respx.mock
    async def test_async_list_customers_with_params(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_LIST_RESPONSE)
        )

        customers = await async_client.customers.list(
            page=1, cpf_cnpj="12345678901", name="Maria"
        )

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 1
        assert isinstance(customers[0], Customer)
        assert customers[0].cpf_cnpj == "12345678901"

    @respx.mock
    async def test_async_list_customers_with_inexisting_cpf(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json={"customers": []})
        )

        customers = await async_client.customers.list(
            cpf_cnpj="00000000000",
        )

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 0


class TestAsyncCustomersGet:
    @respx.mock
    async def test_async_get_customer(self, async_client: AsyncCredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.get(1)

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1


class TestAsyncCustomersFind:
    @respx.mock
    async def test_async_find_customer(self, async_client: AsyncCredereClient) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.find(cpf_cnpj="12345678901")

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"

    @respx.mock
    async def test_async_find_customer_with_params(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.find(cpf_cnpj="12345678901")

        assert route.called
        assert isinstance(customer, Customer)
        assert customer.id == 1
        assert customer.cpf_cnpj == "12345678901"

    @respx.mock
    async def test_async_find_customer_with_inexisting_cpf(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(
                404,
                json={
                    "error": {
                        "message": "Couldn't find Customer",
                        "class": "ActiveRecord::RecordNotFound",
                        "status": 404,
                    }
                },
            )
        )

        with pytest.raises(NotFoundError) as exc:
            await async_client.customers.find(cpf="00000000000")

        assert route.called
        assert exc.value.status_code == 404
