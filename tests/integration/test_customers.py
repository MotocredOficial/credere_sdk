"""Integration tests for the Customers resource.

Run directly:
    python tests/integration/test_customers.py
"""

import random

import pytest

from credere.client import CredereClient
from credere.models.customers import (
    Accountant,
    Address,
    CustomerData,
    CustomerResponse,
    Email,
    JobReference,
    Phone,
)

from .config import EXISTING_CPF, STORE_ID

BANK_LIST = ["623"]  # febraban code from the reference JSON
CUSTOMER_ID = 2474303  # Already existing customer


@pytest.fixture(scope="module")
def generated_cpf() -> str:
    def calc_digit(digits):
        weight = len(digits) + 1
        total = sum(int(d) * (weight - i) for i, d in enumerate(digits))
        remainder = (total * 10) % 11
        return str(remainder if remainder < 10 else 0)

    base = [str(random.randint(0, 9)) for _ in range(9)]

    first_digit = calc_digit(base)
    second_digit = calc_digit([*base, first_digit])

    return "".join([*base, first_digit, second_digit])


@pytest.fixture(scope="module")
def customer_data(generated_cpf: str) -> CustomerData:
    return CustomerData(
        # Identity
        cpf=generated_cpf,
        name="Teste",
        born_at="11/11/1991",
        mother="Testa",
        # Document
        document_type="RG",
        rg="38.551.225-9",
        rg_issuing="ITEP",
        rg_state_id=2,
        # Civil / demographic
        marital_status_id=2,
        spouse_name="Testudo",
        spouse_cpf="662.189.990-41",
        spouse_born_at="19/02/1990",
        nationality="Brasileira",
        place_of_birth="Maceio",
        state_of_birth_id=2,
        genre_id=2,
        # Flags
        public_person=False,
        # Contact
        emails=[Email(address="example@example.com")],
        phones=[
            Phone(code=11, number=999999999, phone_type_id=1),
            Phone(code=11, number=999999992, phone_type_id=2),
        ],
        # Address
        address=Address(
            address_type_id=1,
            zip_code="59032-445",
            state_id=20,
            city="Natal",
            neighborhood="Alecrim",
            street="Avenida Nevaldo Rocha",
            number="2615",
            build_type_id=6,
            rent_value_cents=0,
            set_time_month=24,
            set_time_year=2,
        ),
        # Employment
        job_reference=JobReference(
            professional_ocupation_id=7,
            profession_id=1,
            name="Agro LTDA",
            department="Vendas",
            cnpj="83.877.035/0001-30",
            income_cents=200000,
            another_income_cents=0,
        ),
        personal_references=[],
        accountant=Accountant(name="", city=""),
    )


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_customer(
    sync_client: CredereClient, customer_data: CustomerData
) -> None:
    customer = sync_client.customers.create(customer_data, BANK_LIST, store_id=STORE_ID)
    assert isinstance(customer, CustomerResponse)
    assert customer.id
    assert customer.name
    print(f"  [OK] create_customer — id={customer.id}, name={customer.name}")


def test_get_customer(sync_client: CredereClient) -> None:
    customer = sync_client.customers.get(CUSTOMER_ID, store_id=STORE_ID)
    assert isinstance(customer, CustomerResponse)
    assert customer.id == CUSTOMER_ID
    print(f"  [OK] get_customer — id={customer.id}")


def test_find_customer(sync_client: CredereClient, customer_data: CustomerData) -> None:
    cpf = (
        f"{EXISTING_CPF[:3]}.{EXISTING_CPF[3:6]}.{EXISTING_CPF[6:9]}-{EXISTING_CPF[9:]}"
    )
    customer = sync_client.customers.find(cpf=cpf, store_id=STORE_ID)
    assert isinstance(customer, CustomerResponse)
    assert customer.cpf == cpf
    print(f"  [OK] find_customer — id={customer.id}, cpf={customer.cpf}")


def test_list_customers(sync_client: CredereClient) -> None:
    customers = sync_client.customers.list(store_id=STORE_ID)
    assert isinstance(customers, list)
    print(f"  [OK] list_customers — {len(customers)} customer(s) returned")


def test_domains(sync_client: CredereClient) -> None:
    domains = sync_client.customers.domains()
    assert isinstance(domains, dict)
    print(f"  [OK] get_domains — {len(domains)} domain(s) returned")
    print(f"  Domains - {domains.keys()}")
