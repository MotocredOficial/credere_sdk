"""Integration tests for the Leads resource.

Run directly:
    python tests/integration/test_leads.py
"""

import random

import pytest

from credere.client import CredereClient
from credere.models.leads import Address, LeadData, LeadRequiredFields, LeadResponse

from .config import STORE_ID

# ---------------------------------------------------------------------------
# Fake data — replace with real values before running
# ---------------------------------------------------------------------------


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
def lead_data(generated_cpf: str) -> LeadData:
    return LeadData(
        cpf_cnpj=generated_cpf,
        name="sync_client name",
        birthdate="1970-01-01",
        email="cliente@email.com",
        phone_number="(84) 90000-0000",
        monthly_income=900000,
        has_cnh=True,
        retrieve_gender="F",
        retrieve_occupation="11",
        retrieve_profession="administrador",
        address=Address(
            zip_code="59075-810",
            city="Natal",
            state="RN",
            district="Lagoa Nova",
            street="Av Amintas Barros",
            number="3700, Sala 409 Bloco A",
            complement="Edif Corporate Tower Edif Center-Trade",
        ),
    )


@pytest.fixture(scope="module")
def created_lead(sync_client: CredereClient, lead_data: LeadData) -> LeadResponse:
    lead = sync_client.leads.create(lead_data, store_id=STORE_ID)
    yield lead
    sync_client.leads.delete(lead_data.cpf_cnpj, store_id=STORE_ID)


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_lead(created_lead: LeadResponse) -> None:
    assert isinstance(created_lead, LeadResponse)
    assert created_lead.cpf_cnpj is not None


def test_get_lead(sync_client: CredereClient, created_lead: LeadResponse) -> None:
    cpf = created_lead.cpf_cnpj
    lead = sync_client.leads.get(cpf, store_id=STORE_ID)
    assert isinstance(lead, LeadResponse)
    assert lead.cpf_cnpj is not None
    print(f"  [OK] get_lead — id={lead.id}")


def test_list_leads(sync_client: CredereClient, created_lead: LeadResponse) -> None:
    leads = sync_client.leads.list(store_id=STORE_ID)
    assert isinstance(leads, list)
    print(f"  [OK] list_leads — {len(leads)} lead(s) returned")


def test_update_lead(
    sync_client: CredereClient, lead_data: LeadData, created_lead: LeadResponse
) -> None:
    cpf = lead_data.cpf_cnpj
    update_data = lead_data.model_copy()
    update_data.name = "Nome atualizado"
    lead = sync_client.leads.update(cpf, update_data, store_id=STORE_ID)
    assert isinstance(lead, LeadResponse)
    assert lead.name == "Nome atualizado"
    print(f"  [OK] update_lead — id={lead.id}")


def test_required_fields(sync_client: CredereClient, lead_data: LeadData) -> None:
    cpf = lead_data.cpf_cnpj
    result = sync_client.leads.required_fields(cpf, store_id=STORE_ID)
    assert isinstance(result, LeadRequiredFields)
    print(
        f"""
        [OK] required_fields — requirements keys:
        {list((result.requirements or {}).keys())}
        """
    )


def test_domains(sync_client: CredereClient) -> None:
    result = sync_client.leads.domains()
    assert isinstance(result, dict)
    print(
        f"""
        [OK] domains — domain keys:
        {list(result.keys())}
        """
    )
