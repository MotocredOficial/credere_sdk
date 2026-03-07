"""Tests for the Customers resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.customers import CustomerData, CustomerResponse

BASE_URL = "https://app.meucredere.com.br"
CUSTOMERS_URL = f"{BASE_URL}/api/v1/customers"

SAMPLE_CUSTOMER_CREATE_DATA = {
    "bank_validations": {
        "bank_codes": [
            "033",
            "341",
            "342",
            "394",
            "422",
            "623",
            "655",
            "fontecred",
            "M22",
            "moneyplus",
        ],
        "store_id": 1,
    },
    "customer": {
        "cpf": "000.000.000-00",
        "name": "Nome do cliente",
        "nickname": "Apelido do cliente",
        "born_at": "01/01/2000",
        "have_bank_account": True,
        "accountant": {
            "name": "Nome do contador",
            "city": "Cidade do contador",
            "phone": {
                "code": 84,
                "number": 999999999,
                "phone_type_id": 1,
                "phone_confirmation_id": None,
            },
        },
        "address": {
            "address_type_id": 1,
            "city": "Natal",
            "number": "3700, Sala 409 Bloco A",
            "street": "Avenida Amintas Barros",
            "zip_code": "59075-810",
            "complement": "Edifício Corporate Tower Center-Trade",
            "state_id": 20,
            "neighborhood": "Lagoa Nova",
            "set_time_year": 1,
            "set_time_month": 0,
            "build_type_id": 3,
            "rent_value_cents": 100000,
        },
        "has_made_funding": True,
        "previous_funding_bank_id": 1,
        "accept_boleto": True,
        "note": "Observação",
        "emails": [{"address": "cliente@email.com"}],
        "phones": [
            {
                "code": 84,
                "number": 999999999,
                "phone_type_id": 1,
                "phone_confirmation_id": None,
            },
            {
                "code": 84,
                "number": 999999999,
                "phone_type_id": 2,
                "phone_confirmation_id": None,
            },
        ],
        "bank_references": [
            {
                "bank_id": 1,
                "overdraft": True,
                "agency": "0000-0",
                "open_at": "01/01/2000",
                "account_number": "00000",
                "digit": "0",
            }
        ],
        "addresses": [
            {
                "address_type_id": 2,
                "city": "Natal",
                "number": "3700, Sala 409 Bloco A",
                "street": "Avenida Amintas Barros",
                "zip_code": "59075-810",
                "complement": "Edifício Corporate Tower Center-Trade",
                "state_id": 20,
                "neighborhood": "Lagoa Nova",
                "set_time_year": 1,
                "set_time_month": 0,
                "build_type_id": 3,
                "rent_value_cents": 100000,
            },
            {
                "address_type_id": 3,
                "city": "Natal",
                "number": "3700, Sala 409 Bloco A",
                "street": "Avenida Amintas Barros",
                "zip_code": "59075-810",
                "complement": "Edifício Corporate Tower Center-Trade",
                "state_id": 20,
                "neighborhood": "Lagoa Nova",
            },
        ],
        "attachments": [],
        "mother": "Nome da mãe",
        "father": "Nome do pai",
        "document_type": "RG",
        "rg": "000000000",
        "rg_date": "01/01/2000",
        "rg_state_id": 20,
        "rg_issuing": "SSP",
        "has_cnh": True,
        "cnh": "00000000000",
        "cnh_type_id": 1,
        "marital_status_id": 1,
        "spouse_name": "Nome do cônjuge",
        "spouse_born_at": "01/01/2000",
        "spouse_cpf": "000.000.000-00",
        "nationality": "Brasileira",
        "place_of_birth": "Natal",
        "state_of_birth_id": 20,
        "genre_id": 1,
        "education_id": 5,
        "property": 4,
        "public_person": True,
        "job_reference": {
            "address": {
                "address_type_id": 4,
                "city": "Natal",
                "number": "3700, Sala 409 Bloco A",
                "street": "Avenida Amintas Barros",
                "zip_code": "59075-810",
                "complement": "Edifício Corporate Tower Center-Trade",
                "state_id": 20,
                "neighborhood": "Lagoa Nova",
            },
            "joined_at": "01/01/2010",
            "income_cents": 1000000,
            "another_income_cents": 100000,
            "another_income_type_id": 2,
            "detail": "",
            "first_job": False,
            "professional_ocupation_id": 6,
            "profession_id": 2,
            "department": "Nome do departamento",
            "name": "Nome da empresa",
            "cnpj": "00.000.000/0000-00",
            "company_activity_id": 2,
            "phone": {
                "code": 84,
                "number": 999999999,
                "phone_type_id": 3,
                "phone_confirmation_id": None,
            },
            "previous_work": "Nome da empresa",
            "previous_work_start_at": "01/01/2000",
            "previous_work_end_at": "01/01/2000",
            "previous_job_phone": {
                "code": 84,
                "number": 999999999,
                "phone_type_id": 5,
                "phone_confirmation_id": None,
            },
        },
        "have_credit_card": True,
        "credit_cards": "Mastercard",
        "personal_references": [
            {
                "name": "Nome do contato de referência",
                "city": "Natal",
                "phone": {
                    "code": 84,
                    "number": 999999999,
                    "phone_type_id": 2,
                    "phone_confirmation_id": None,
                },
                "relationship": "Pai",
            }
        ],
    },
}

SAMPLE_CUSTOMER_RESPONSE = {
    "customer": {
        "object_type": "Customer",
        "id": 1,
        "created_at": "2000-01-01T00:00:00.000-03:00",
        "updated_at": "22000-01-01T00:00:00.000-03:00",
        "name": "Nome do cliente",
        "cpf": "000.000.000-00",
        "have_bank_account": True,
        "have_credit_card": True,
        "has_made_funding": True,
        "property": 4,
        "public_person": True,
        "born_at": "2000-01-01",
        "rg": "000000000",
        "rg_date": "2000-01-01",
        "rg_state_id": 20,
        "genre_id": 1,
        "mother": "Nome da mãe",
        "education_id": 5,
        "marital_status_id": 1,
        "place_of_birth": "Natal",
        "state_of_birth_id": 20,
        "document_type": "RG",
        "rg_issuing": "SSP",
        "cnh": "00000000000",
        "cnh_type_id": 1,
        "nationality": "Brasileira",
        "note": "Observação",
        "accept_boleto": True,
        "nickname": "Apelido do cliente",
        "father": "Nome do pai",
        "has_cnh": True,
        "credit_cards": "Mastercard",
        "previous_funding_bank_id": 116,
        "spouse_name": "Nome do cônjuge",
        "spouse_born_at": "2000-01-01",
        "spouse_cpf": "000.000.000-00",
        "state": "checagem",
        "creation_external_link_id": None,
        "cnpj": None,
        "joint_stock_cents": None,
        "ie": None,
        "im": None,
        "company_activity_id": None,
        "rg_state": {"id": 20, "name": "Rio Grande do Norte", "abbreviation": "RN"},
        "genre": {"id": 1, "name": "Masculino"},
        "marital_status": {"id": 1, "name": "Casado", "honda_code": "C"},
        "education": {
            "id": 5,
            "name": "Ensino Superior",
            "honda_code": "SUP",
            "identifier": "7",
        },
        "state_of_birth": {
            "id": 20,
            "name": "Rio Grande do Norte",
            "abbreviation": "RN",
        },
        "cnh_type": {"id": 1, "name": "A"},
        "company_activity": {
            "object_type": "CompanyActivity",
            "id": 2,
            "created_at": "2000-01-01T00:00:00.000-03:00",
            "updated_at": "2000-01-01T00:00:00.000-03:00",
            "name": "Comércio",
        },
        "accountant": {
            "id": 2,
            "object_type": "PersonalReference",
            "created_at": "2000-01-01T00:00:00.000-03:00",
            "updated_at": "2000-01-01T00:00:00.000-03:00",
            "name": "Nome do contador",
            "relationship": "Contador",
            "city": "Cidade do contador",
            "phone": {
                "id": 6,
                "object_type": "Phone",
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "code": 84,
                "number": 999999999,
                "phone_type": {
                    "object_type": "PhoneType",
                    "id": 1,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Celular",
                },
                "phone_confirmation": None,
            },
        },
        "address": {
            "object_type": "Address",
            "id": 1,
            "created_at": "2000-01-01T00:00:00.000-03:00",
            "updated_at": "2000-01-01T00:00:00.000-03:00",
            "city": "Natal",
            "complement": "Edifício Corporate Tower Center-Trade",
            "number": "3700, Sala 409 Bloco A",
            "reference": None,
            "street": "Avenida Amintas Barros",
            "set_time_month": 8,
            "set_time_year": 22,
            "neighborhood": "Lagoa Nova",
            "zip_code": "59075-810",
            "rent_value_cents": 100000,
            "neighbourhood": "Lagoa Nova",
            "state": {
                "object_type": "State",
                "id": 20,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Rio Grande do Norte",
                "abbreviation": "RN",
            },
            "build_type": {
                "object_type": "BuildType",
                "id": 3,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Alugada",
            },
            "address_type": {
                "object_type": "AddressType",
                "id": 1,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Principal",
            },
        },
        "job_reference": {
            "object_type": "JobReference",
            "id": 1,
            "created_at": "2000-01-01T00:00:00.000-03:00",
            "updated_at": "2000-01-01T00:00:00.000-03:00",
            "joined_at": "2010-01-01",
            "income_cents": 1000000,
            "another_income_type": {
                "object_type": "AnotherIncomeType",
                "id": 2,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Aplicações",
            },
            "detail": "",
            "department": "Nome do departamento",
            "name": "Nome da empresa",
            "cnpj": "",
            "first_job": False,
            "previous_work": "Nome da empresa",
            "previous_work_start_at": "2000-01-01",
            "previous_work_end_at": "2000-01-01",
            "previous_job_phone": {
                "object_type": "Phone",
                "id": 4,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "code": 84,
                "number": 999999999,
                "phone_type": {
                    "object_type": "PhoneType",
                    "id": 6,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Empresa Anterior",
                },
                "phone_confirmation": None,
            },
            "another_income_cents": 100000,
            "address": {
                "object_type": "Address",
                "id": 4,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "city": "Natal",
                "complement": "Edifício Corporate Tower Center-Trade",
                "number": "3700, Sala 409 Bloco A",
                "reference": None,
                "street": "Avenida Amintas Barros",
                "set_time_month": None,
                "set_time_year": None,
                "neighborhood": "Lagoa Nova",
                "zip_code": "59075-810",
                "rent_value_cents": None,
                "neighbourhood": "Lagoa Nova",
                "state": {
                    "object_type": "State",
                    "id": 20,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Rio Grande do Norte",
                    "abbreviation": "RN",
                },
                "build_type": None,
                "address_type": {
                    "object_type": "AddressType",
                    "id": 4,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Comercial",
                },
            },
            "phone": {
                "object_type": "Phone",
                "id": 3,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "code": 84,
                "number": 999999999,
                "phone_type": {
                    "object_type": "PhoneType",
                    "id": 4,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Comercial",
                },
                "phone_confirmation": None,
            },
            "profession": {
                "object_type": "Profession",
                "id": 2,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "ADMINISTRADOR",
                "identifier": "administrador",
            },
            "company_activity": {
                "object_type": "CompanyActivity",
                "id": 2,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Comércio",
            },
            "professional_ocupation": {
                "object_type": "ProfessionalOcupation",
                "id": 6,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Profissional Liberal",
                "identifier": "100",
            },
        },
        "previous_funding_bank": {
            "object_type": "Bank",
            "id": 116,
            "created_at": "2000-01-01T00:00:00.000-03:00",
            "updated_at": "2000-01-01T00:00:00.000-03:00",
            "name": "Banco do Brasil S.A.",
            "tradename": "BB",
            "code": "001",
        },
        "addresses": [
            {
                "object_type": "Address",
                "id": 3,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "city": "Natal",
                "complement": "Edifício Corporate Tower Center-Trade",
                "number": "3700, Sala 409 Bloco A",
                "reference": None,
                "street": "Avenida Amintas Barros",
                "set_time_month": None,
                "set_time_year": None,
                "neighborhood": "Lagoa Nova",
                "zip_code": "59075-810",
                "rent_value_cents": None,
                "neighbourhood": "Lagoa Nova",
                "state": {
                    "object_type": "State",
                    "id": 20,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Rio Grande do Norte",
                    "abbreviation": "RN",
                },
                "build_type": None,
                "address_type": {
                    "object_type": "AddressType",
                    "id": 3,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Alternativo",
                },
            },
            {
                "object_type": "Address",
                "id": 2,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "city": "Natal",
                "complement": "Edifício Corporate Tower Center-Trade",
                "number": "3700, Sala 409 Bloco A",
                "reference": None,
                "street": "Avenida Amintas Barros",
                "set_time_month": 8,
                "set_time_year": 22,
                "neighborhood": "Lagoa Nova",
                "zip_code": "59075-810",
                "rent_value_cents": 100000,
                "neighbourhood": "Lagoa Nova",
                "state": {
                    "object_type": "State",
                    "id": 20,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Rio Grande do Norte",
                    "abbreviation": "RN",
                },
                "build_type": {
                    "object_type": "BuildType",
                    "id": 3,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Alugada",
                },
                "address_type": {
                    "object_type": "AddressType",
                    "id": 2,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Anterior",
                },
            },
        ],
        "bank_references": [
            {
                "object_type": "BankReference",
                "id": 1,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "overdraft": True,
                "agency": "0000-0",
                "open_at": "2000-01-01",
                "account_number": "00000",
                "digit": "0",
                "bank": {
                    "object_type": "Bank",
                    "id": 116,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Banco do Brasil S.A.",
                    "tradename": "BB",
                    "code": "001",
                },
            }
        ],
        "emails": [
            {
                "object_type": "Email",
                "id": 1,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "address": "cliente@email.com",
            }
        ],
        "guarantors": [],
        "personal_references": [
            {
                "object_type": "PersonalReference",
                "id": 1,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "name": "Nome do contato de referência",
                "relationship": "Pai",
                "city": "Natal",
                "phone": {
                    "object_type": "Phone",
                    "id": 30,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "code": 84,
                    "number": 999999999,
                    "phone_type": {
                        "object_type": "PhoneType",
                        "id": 5,
                        "created_at": "2000-01-01T00:00:00.000-03:00",
                        "updated_at": "2000-01-01T00:00:00.000-03:00",
                        "name": "Principal",
                    },
                    "phone_confirmation": None,
                },
            }
        ],
        "phones": [
            {
                "object_type": "Phone",
                "id": 1,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "code": 84,
                "number": 999999999,
                "phone_type": {
                    "object_type": "PhoneType",
                    "id": 1,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Celular",
                },
                "phone_confirmation": None,
            },
            {
                "object_type": "Phone",
                "id": 2,
                "created_at": "2000-01-01T00:00:00.000-03:00",
                "updated_at": "2000-01-01T00:00:00.000-03:00",
                "code": 84,
                "number": 999999999,
                "phone_type": {
                    "object_type": "PhoneType",
                    "id": 2,
                    "created_at": "2000-01-01T00:00:00.000-03:00",
                    "updated_at": "2000-01-01T00:00:00.000-03:00",
                    "name": "Principal",
                },
                "phone_confirmation": None,
            },
        ],
        "attachments": [],
        "monthly_billings": [],
        "partners": [],
    }
}

SAMPLE_CUSTOMER_LIST_RESPONSE = {"customers": [SAMPLE_CUSTOMER_RESPONSE["customer"]]}


class TestCustomersCreate:
    @respx.mock
    def test_create_customer(self, sync_client: CredereClient) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer_data = CustomerData.model_validate(
            SAMPLE_CUSTOMER_CREATE_DATA["customer"]
        )
        bank_list = ["M123", "M456"]
        customer = sync_client.customers.create(customer_data, bank_list)

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.cpf == "000.000.000-00"
        assert customer.name == "Nome do cliente"


class TestCustomersUpdate:
    @respx.mock
    def test_update_customer(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        updated_data = SAMPLE_CUSTOMER_RESPONSE["customer"].copy()
        updated_data["name"] = "Nome do cliente atualizado"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json={"customer": updated_data})
        )

        customer_data = CustomerData.model_validate(
            SAMPLE_CUSTOMER_CREATE_DATA["customer"]
        )
        bank_list = ["M123", "M456"]
        customer_data.name = "Nome do cliente atualizado"
        customer = sync_client.customers.update(1, customer_data, bank_list)

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.name == "Nome do cliente atualizado"


class TestCustomersList:
    @respx.mock
    def test_list_customers(self, sync_client: CredereClient) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_LIST_RESPONSE)
        )

        customers = sync_client.customers.list()

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 1
        assert isinstance(customers[0], CustomerResponse)
        assert customers[0].cpf == "000.000.000-00"

    @respx.mock
    def test_list_customers_with_inexisting_cpf(
        self, sync_client: CredereClient
    ) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json={"customers": []})
        )

        customers = sync_client.customers.list(
            cpf_cnpj="00000000001",
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
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.name == "Nome do cliente"


class TestCustomersFind:
    @respx.mock
    def test_find_customer(self, sync_client: CredereClient) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = sync_client.customers.find(cpf_cnpj="000000000000")

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.cpf == "000.000.000-00"

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


class TestAsyncCustomersCreate:
    @pytest.mark.asyncio
    @respx.mock
    async def test_create_customer(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer_data = CustomerData.model_validate(
            SAMPLE_CUSTOMER_CREATE_DATA["customer"]
        )
        bank_list = ["M123", "M456"]
        customer = await async_client.customers.create(customer_data, bank_list)

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.cpf == "000.000.000-00"
        assert customer.name == "Nome do cliente"


class TestAsyncCustomersUpdate:
    @pytest.mark.asyncio
    @respx.mock
    async def test_update_customer(self, async_client: AsyncCredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        updated_data = SAMPLE_CUSTOMER_RESPONSE["customer"].copy()
        updated_data["name"] = "Nome do cliente atualizado"
        route = respx.patch(url).mock(
            return_value=httpx.Response(200, json={"customer": updated_data})
        )

        customer_data = CustomerData.model_validate(
            SAMPLE_CUSTOMER_CREATE_DATA["customer"]
        )
        customer_data.name = "Nome do cliente atualizado"
        customer = await async_client.customers.update(1, customer_data)

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.name == "Nome do cliente atualizado"


class TestAsyncCustomersList:
    @pytest.mark.asyncio
    @respx.mock
    async def test_list_customers(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_LIST_RESPONSE)
        )

        customers = await async_client.customers.list()

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 1
        assert isinstance(customers[0], CustomerResponse)
        assert customers[0].cpf == "000.000.000-00"

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_customers_with_inexisting_cpf(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(200, json={"customers": []})
        )

        customers = await async_client.customers.list(
            cpf_cnpj="00000000001",
        )

        assert route.called
        assert isinstance(customers, list)
        assert len(customers) == 0


class TestAsyncCustomersGet:
    @pytest.mark.asyncio
    @respx.mock
    async def test_get_customer(self, async_client: AsyncCredereClient) -> None:
        url = f"{CUSTOMERS_URL}/1"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.get(1)

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.name == "Nome do cliente"


class TestAsyncCustomersFind:
    @pytest.mark.asyncio
    @respx.mock
    async def test_find_customer(self, async_client: AsyncCredereClient) -> None:
        url = f"{CUSTOMERS_URL}/find"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER_RESPONSE)
        )

        customer = await async_client.customers.find(cpf_cnpj="000000000000")

        assert route.called
        assert isinstance(customer, CustomerResponse)
        assert customer.id == 1
        assert customer.cpf == "000.000.000-00"

    @pytest.mark.asyncio
    @respx.mock
    async def test_find_customer_with_inexisting_cpf(
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


class TestCustomersDomains:
    @respx.mock
    def test_domains_without_filter(self, sync_client: CredereClient) -> None:
        domains_url = f"{BASE_URL}/api/v1/domains"
        route = respx.get(domains_url).mock(
            return_value=httpx.Response(
                200,
                json={
                    "domains": {
                        "genders": [
                            {"id": 1, "name": "Masculino", "identifier": "M"},
                            {"id": 2, "name": "Feminino", "identifier": "F"},
                        ],
                        "marital_statuses": [
                            {"id": 1, "name": "Casado"},
                        ],
                    }
                },
            )
        )

        result = sync_client.customers.domains()

        assert route.called
        assert "genders" in result
        assert "marital_statuses" in result
        assert len(result["genders"]) == 2
        assert result["genders"][0].id == 1
        assert result["genders"][0].name == "Masculino"
        assert result["genders"][0].identifier == "M"
        assert result["marital_statuses"][0].name == "Casado"

    @respx.mock
    def test_domains_with_types_filter(self, sync_client: CredereClient) -> None:
        domains_url = f"{BASE_URL}/api/v1/domains"
        route = respx.get(domains_url).mock(
            return_value=httpx.Response(
                200,
                json={
                    "domains": {
                        "genders": [
                            {"id": 1, "name": "Masculino"},
                        ],
                    }
                },
            )
        )

        result = sync_client.customers.domains(types=["genders", "marital_statuses"])

        assert route.called
        # Verify the types param was joined with comma
        request = route.calls.last.request
        assert "types=genders%2Cmarital_statuses" in str(request.url)
        assert "genders" in result


class TestAsyncCustomersDomains:
    @pytest.mark.asyncio
    @respx.mock
    async def test_async_domains(self, async_client: AsyncCredereClient) -> None:
        domains_url = f"{BASE_URL}/api/v1/domains"
        route = respx.get(domains_url).mock(
            return_value=httpx.Response(
                200,
                json={
                    "domains": {
                        "genders": [
                            {"id": 1, "name": "Masculino", "identifier": "M"},
                        ],
                    }
                },
            )
        )

        result = await async_client.customers.domains()

        assert route.called
        assert "genders" in result
        assert result["genders"][0].id == 1
        assert result["genders"][0].name == "Masculino"


class TestAsyncErrorMapping:
    @pytest.mark.asyncio
    @respx.mock
    async def test_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(CUSTOMERS_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await async_client.customers.list()

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    @respx.mock
    async def test_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
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
            await async_client.customers.get(99999)

        assert exc_info.value.status_code == 404
