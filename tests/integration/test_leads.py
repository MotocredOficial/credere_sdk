"""Integration tests for the Leads resource.

Run directly:
    python tests/integration/test_leads.py
"""

import pytest

from credere.client import CredereClient
from credere.models.leads import Address, LeadData, LeadRequiredFields, LeadResponse

from .config import CLIENT_CPF, STORE_ID

# ---------------------------------------------------------------------------
# Fake data — replace with real values before running
# ---------------------------------------------------------------------------

LEAD_CPF = CLIENT_CPF


@pytest.fixture
def created_lead(sync_client: CredereClient) -> None:
    lead_data = LeadData(
        cpf_cnpj=LEAD_CPF,
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

    lead = sync_client.leads.create(lead_data, store_id=STORE_ID)
    yield lead
    sync_client.leads.delete(LEAD_CPF, store_id=STORE_ID)


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------


def test_create_lead(created_lead):
    assert isinstance(created_lead, LeadResponse)
    assert created_lead.cpf_cnpj is not None


def test_get_lead(sync_client, created_lead) -> None:
    lead = sync_client.leads.get(LEAD_CPF, store_id=STORE_ID)
    assert isinstance(lead, LeadResponse)
    assert lead.cpf_cnpj is not None
    print(f"  [OK] get_lead — id={lead.id}")


def test_list_leads(sync_client, created_lead) -> None:
    leads = sync_client.leads.list(store_id=STORE_ID)
    assert isinstance(leads, list)
    print(f"  [OK] list_leads — {len(leads)} lead(s) returned")


def test_update_lead(sync_client, created_lead) -> None:
    update_data = created_lead
    update_data.name = "Nome atualizado"
    lead = sync_client.leads.update(LEAD_CPF, update_data, store_id=STORE_ID)
    assert isinstance(lead, LeadResponse)
    assert lead.name == "Nome atualizado"
    print(f"  [OK] update_lead — id={lead.id}")


def test_required_fields(sync_client, created_lead) -> None:
    result = sync_client.leads.required_fields(LEAD_CPF, store_id=STORE_ID)
    assert isinstance(result, LeadRequiredFields)
    print(
        f"""
        [OK] required_fields — requirements keys:
        {list((result.requirements or {}).keys())}
        """
    )


def test_domains(sync_client) -> None:
    result = sync_client.leads.domains()
    assert isinstance(result, dict)
    print(
        f"""
        [OK] domains — domain keys:
        {list(result.keys())}
        """
    )
