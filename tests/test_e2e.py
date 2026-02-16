"""E2E test — full SDK workflow exercising every resource and method."""

import json

import httpx
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.models.bank_credentials import IntegratedBank
from credere.models.customers import Customer, CustomerCreateRequest
from credere.models.leads import Lead, LeadCreateRequest, LeadRequiredFields
from credere.models.plus_returns import (
    PlusReturnRule,
    PlusReturnRuleCreateRequest,
)
from credere.models.proposal_attempts import (
    ProposalAttempt,
    ProposalAttemptCreateRequest,
)
from credere.models.proposals import (
    Proposal,
    ProposalConditionRequest,
    ProposalCreateRequest,
    ProposalVehicleRequest,
)
from credere.models.simulations import (
    Bank,
    Simulation,
    SimulationConditionRequest,
    SimulationCreateRequest,
    SimulationVehicleRequest,
)
from credere.models.stock import StockVehicle, StockVehicleCreateRequest
from credere.models.stores import Store, StoreCreateRequest
from credere.models.users import User
from credere.models.utilities import Domain
from credere.models.vehicle_models import VehicleModel, VehiclePrice

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

BASE_URL = "https://api.credere.com"
STORE_ID = 1
CUSTOMER_ID = 10
LEAD_CPF = "12345678900"
SIMULATION_UUID = "sim-uuid-001"
PROPOSAL_ID = "prop-uuid-001"
ATTEMPT_ID = "1"
STOCK_VEHICLE_ID = 500
PLUS_RETURN_ID = 200
VEHICLE_MODEL_ID = 300
CHASSI_CODE = "9BWZZZ377VT004251"

# Derived URL constants for long paths
PA_URL = f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/proposal_attempts"

# ---------------------------------------------------------------------------
# Request data objects
# ---------------------------------------------------------------------------

STORE_CREATE_DATA = StoreCreateRequest(
    name="Loja Central",
    display_name="Central",
    cnpj="11222333000181",
)

CUSTOMER_CREATE_DATA = CustomerCreateRequest(
    cpf_cnpj="12345678900",
    name="Joao Silva",
    birthdate="1990-05-20",
    email="joao@example.com",
    phone_number="11999998888",
    monthly_income=600000,
)

CUSTOMER_UPDATE_DATA = CustomerCreateRequest(
    name="Joao Silva Atualizado",
)

LEAD_CREATE_DATA = LeadCreateRequest(
    cpf_cnpj="12345678900",
    name="Joao Silva",
    birthdate="1990-05-20",
    email="joao@example.com",
    phone_number="11999998888",
    monthly_income=600000,
)

LEAD_UPDATE_DATA = LeadCreateRequest(
    name="Joao Atualizado",
)

SIMULATION_CREATE_DATA = SimulationCreateRequest(
    assets_value=7000000,
    documentation_value=50000,
    seller_cpf="99988877766",
    retrieve_lead={"cpf_cnpj": "12345678900"},
    conditions=[
        SimulationConditionRequest(
            down_payment=1500000,
            financed_amount=5500000,
            installments=48,
        ),
    ],
    vehicle=SimulationVehicleRequest(
        asset_value=7000000,
        licensing_uf="SP",
        manufacture_year=2024,
        model_year=2024,
        vehicle_molicar_code="MOL456",
        zero_km=True,
    ),
)

PROPOSAL_CREATE_DATA = ProposalCreateRequest(
    assets_value=7000000,
    documentation_value=50000,
    seller_cpf="99988877766",
    retrieve_lead={"cpf_cnpj": "12345678900"},
    conditions=[
        ProposalConditionRequest(
            down_payment=1500000,
            financed_amount=5500000,
            installments=48,
        ),
    ],
    vehicle=ProposalVehicleRequest(
        asset_value=7000000,
        licensing_uf="SP",
        manufacture_year=2024,
        model_year=2024,
        vehicle_molicar_code="MOL456",
        zero_km=True,
    ),
)

ATTEMPT_CREATE_DATA = ProposalAttemptCreateRequest()
ATTEMPT_UPDATE_DATA = ProposalAttemptCreateRequest()

STOCK_CREATE_DATA = StockVehicleCreateRequest(
    vehicle_model_id=300,
    store_id=1,
    price_cents=7000000,
    description="Fiat Argo 1.0 2024",
)

STOCK_UPDATE_DATA = StockVehicleCreateRequest(
    price_cents=7500000,
)

PLUS_RETURN_CREATE_DATA = PlusReturnRuleCreateRequest()
PLUS_RETURN_UPDATE_DATA = PlusReturnRuleCreateRequest()

# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

USER_RESP = {
    "id": 1,
    "name": "Admin",
    "email": "admin@loja.com",
}

STORE_RESP = {
    "id": 1,
    "name": "Loja Central",
    "display_name": "Central",
    "cnpj": "11222333000181",
}

CUSTOMER_RESP = {
    "id": 10,
    "cpf_cnpj": "12345678900",
    "name": "Joao Silva",
    "email": "joao@example.com",
    "phone_number": "11999998888",
    "monthly_income": 600000,
    "birthdate": "1990-05-20",
}

CUSTOMER_UPDATED_RESP = {
    **CUSTOMER_RESP,
    "name": "Joao Silva Atualizado",
}

LEAD_RESP = {
    "id": 1,
    "cpf_cnpj": "12345678900",
    "name": "Joao Silva",
    "phone_number": "11999998888",
    "monthly_income": 600000,
}

LEAD_UPDATED_RESP = {**LEAD_RESP, "name": "Joao Atualizado"}

LEAD_REQUIRED_FIELDS_RESP = {
    "lead": {"id": 1, "cpf_cnpj": "12345678900"},
    "requirements": {"mother_name": True},
}

DOMAIN_RESP = {
    "id": 1,
    "type": "gender",
    "credere_identifier": "male",
    "label": "Masculino",
}

BANK_RESP = {
    "id": 1,
    "febraban_code": "001",
    "name": "Banco do Brasil",
    "nickname": "BB",
}

VEHICLE_BY_PLATE_RESP = {
    "plate": "ABC1D23",
    "brand": "Fiat",
    "model": "Argo",
}

VEHICLE_BY_CHASSI_RESP = {
    "chassi": CHASSI_CODE,
    "brand": "Fiat",
    "model": "Argo",
}

VEHICLE_MODEL_RESP = {
    "id": VEHICLE_MODEL_ID,
    "name": "Argo 1.0",
    "brand": "Fiat",
    "molicar_code": "MOL456",
}

VEHICLE_PRICE_RESP = {
    "id": 1,
    "store_id": 1,
    "min_price_cents": 5000000,
    "default_price_cents": 7000000,
    "active": True,
}

INTEGRATED_BANK_RESP = {
    "id": 1,
    "store_id": 1,
    "bank": {"id": 1, "name": "Banco do Brasil"},
    "credentials_status": "active",
}

BANK_PERSIST_RESP = {"persisted": True, "store_id": 1}

SIMULATION_RESP = {
    "assets_value": 7000000,
    "conditions": [
        {
            "id": 1,
            "installments": 48,
            "down_payment": 1500000,
            "financed_amount": 5500000,
        }
    ],
}

PROPOSAL_RESP = {
    "id": PROPOSAL_ID,
    "assets_value": 7000000,
    "documentation_value": 50000,
    "status": "pending",
    "seller_cpf": "99988877766",
}

ACTIVITY_LOG_RESP = [
    {"action": "created", "timestamp": "2024-01-01T00:00:00Z"},
    {"action": "updated", "timestamp": "2024-01-02T00:00:00Z"},
]

ATTEMPT_RESP = {
    "id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

STOCK_VEHICLE_RESP = {
    "id": STOCK_VEHICLE_ID,
    "price_cents": 7000000,
    "description": "Fiat Argo 1.0 2024",
}

STOCK_VEHICLE_UPDATED_RESP = {
    **STOCK_VEHICLE_RESP,
    "price_cents": 7500000,
}

PLUS_RETURN_RESP = {
    "id": PLUS_RETURN_ID,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def assert_store_id(route, expected="42"):
    """Assert the Store-Id header was sent with the expected value."""
    assert route.calls.last.request.headers["Store-Id"] == expected


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------


class TestE2EWorkflow:
    """E2E test exercising every resource and every method."""

    @respx.mock
    def test_sync_full_workflow(self, sync_client: CredereClient) -> None:
        # =============================================================
        # Phase 1: Auth & User Context
        # =============================================================

        # Step 1: users.current()
        r1 = respx.get(f"{BASE_URL}/v1/users/current").mock(
            return_value=httpx.Response(200, json={"user": USER_RESP})
        )
        result = sync_client.users.current()
        assert r1.called
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "Admin"
        assert "Store-Id" not in r1.calls.last.request.headers

        # Step 2: users.proposals_filter_list()
        r2 = respx.get(f"{BASE_URL}/v1/users/proposals_filter_list").mock(
            return_value=httpx.Response(200, json={"users": [USER_RESP]})
        )
        result = sync_client.users.proposals_filter_list()
        assert r2.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], User)
        assert result[0].id == 1
        assert result[0].name == "Admin"
        assert_store_id(r2)

        # =============================================================
        # Phase 2: Store Setup
        # =============================================================

        # Step 3: stores.create()
        r3 = respx.post(f"{BASE_URL}/v1/stores").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = sync_client.stores.create(STORE_CREATE_DATA)
        assert r3.called
        body = json.loads(r3.calls.last.request.content)
        assert "store" in body
        assert body["store"]["name"] == "Loja Central"
        assert body["store"]["display_name"] == "Central"
        assert body["store"]["cnpj"] == "11222333000181"
        assert_store_id(r3)
        assert isinstance(result, Store)
        assert result.id == 1
        assert result.name == "Loja Central"

        # Step 4: stores.list()
        r4 = respx.get(f"{BASE_URL}/v1/stores").mock(
            return_value=httpx.Response(200, json={"stores": [STORE_RESP]})
        )
        result = sync_client.stores.list()
        assert r4.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Store)
        assert result[0].id == 1
        assert_store_id(r4)

        # Step 5: stores.activate(1)
        r5 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/activate").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = sync_client.stores.activate(STORE_ID)
        assert r5.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert_store_id(r5)

        # Step 6: stores.deactivate(1)
        r6 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/deactivate").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = sync_client.stores.deactivate(STORE_ID)
        assert r6.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert_store_id(r6)

        # =============================================================
        # Phase 3: Reference Data
        # =============================================================

        # Step 7: utilities.domains()
        r7 = respx.get(f"{BASE_URL}/v1/domains").mock(
            return_value=httpx.Response(200, json=[DOMAIN_RESP])
        )
        result = sync_client.utilities.domains()
        assert r7.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert result[0].label == "Masculino"
        assert_store_id(r7)

        # Step 8: utilities.lead_domains()
        r8 = respx.get(f"{BASE_URL}/v1/banks_api/domains").mock(
            return_value=httpx.Response(200, json=[DOMAIN_RESP])
        )
        result = sync_client.utilities.lead_domains()
        assert r8.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert_store_id(r8)

        # Step 9: utilities.banks()
        r9 = respx.get(f"{BASE_URL}/v1/banks").mock(
            return_value=httpx.Response(200, json={"banks": [BANK_RESP]})
        )
        result = sync_client.utilities.banks()
        assert r9.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Bank)
        assert result[0].id == 1
        assert result[0].name == "Banco do Brasil"
        assert_store_id(r9)

        # Step 10: utilities.vehicle_by_plate("ABC1D23")
        r10 = respx.get(f"{BASE_URL}/v1/vehicles/license_plate/ABC1D23").mock(
            return_value=httpx.Response(200, json=VEHICLE_BY_PLATE_RESP)
        )
        result = sync_client.utilities.vehicle_by_plate("ABC1D23")
        assert r10.called
        assert isinstance(result, dict)
        assert result["plate"] == "ABC1D23"
        assert result["brand"] == "Fiat"
        assert_store_id(r10)

        # Step 11: utilities.vehicle_by_chassis(...)
        r11 = respx.get(f"{BASE_URL}/v1/vehicles/chassi_code/{CHASSI_CODE}").mock(
            return_value=httpx.Response(200, json=VEHICLE_BY_CHASSI_RESP)
        )
        result = sync_client.utilities.vehicle_by_chassis(CHASSI_CODE)
        assert r11.called
        assert isinstance(result, dict)
        assert result["chassi"] == CHASSI_CODE
        assert result["brand"] == "Fiat"
        assert_store_id(r11)

        # Step 12: vehicle_models.list()
        r12 = respx.get(f"{BASE_URL}/v1/vehicle_models").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_models": [VEHICLE_MODEL_RESP]},
            )
        )
        result = sync_client.vehicle_models.list()
        assert r12.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == VEHICLE_MODEL_ID
        assert result[0].name == "Argo 1.0"
        assert_store_id(r12)

        # Step 13: vehicle_models.search("Argo")
        r13 = respx.get(f"{BASE_URL}/v1/vehicle_models/search").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_model": VEHICLE_MODEL_RESP},
            )
        )
        result = sync_client.vehicle_models.search("Argo")
        assert r13.called
        assert isinstance(result, VehicleModel)
        assert result.molicar_code == "MOL456"
        assert result.id == VEHICLE_MODEL_ID
        assert_store_id(r13)

        # Step 14: vehicle_models.prices()
        r14 = respx.get(f"{BASE_URL}/v1/vehicle_prices").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_prices": [VEHICLE_PRICE_RESP]},
            )
        )
        result = sync_client.vehicle_models.prices()
        assert r14.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehiclePrice)
        assert result[0].id == 1
        assert result[0].default_price_cents == 7000000
        assert_store_id(r14)

        # =============================================================
        # Phase 4: Bank Integration
        # =============================================================

        # Step 15: bank_credentials.persist(1)
        r15 = respx.get(
            f"{BASE_URL}/v1/stores/{STORE_ID}/persist_cnpj_bank_credentials"
        ).mock(return_value=httpx.Response(200, json=BANK_PERSIST_RESP))
        result = sync_client.bank_credentials.persist(STORE_ID)
        assert r15.called
        assert isinstance(result, dict)
        assert result["persisted"] is True
        assert_store_id(r15)

        # Step 16: bank_credentials.list(1)
        r16 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/integrated_banks").mock(
            return_value=httpx.Response(
                200,
                json={"integrated_banks": [INTEGRATED_BANK_RESP]},
            )
        )
        result = sync_client.bank_credentials.list(store_id=STORE_ID)
        assert r16.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], IntegratedBank)
        assert result[0].id == 1
        assert result[0].credentials_status == "active"
        assert_store_id(r16)

        # =============================================================
        # Phase 5: Customer Management
        # =============================================================

        # Step 17: customers.create(data)
        r17 = respx.post(f"{BASE_URL}/v1/customers").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = sync_client.customers.create(CUSTOMER_CREATE_DATA)
        assert r17.called
        body = json.loads(r17.calls.last.request.content)
        assert "customer" in body
        payload = body["customer"]
        assert payload["cpf_cnpj"] == "12345678900"
        assert payload["name"] == "Joao Silva"
        assert payload["birthdate"] == "1990-05-20"
        assert payload["email"] == "joao@example.com"
        assert payload["phone_number"] == "11999998888"
        assert payload["monthly_income"] == 600000
        assert_store_id(r17)
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert result.name == "Joao Silva"

        # Step 18: customers.get(10)
        r18 = respx.get(f"{BASE_URL}/v1/customers/{CUSTOMER_ID}").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = sync_client.customers.get(CUSTOMER_ID)
        assert r18.called
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r18)

        # Step 19: customers.list()
        r19 = respx.get(f"{BASE_URL}/v1/customers").mock(
            return_value=httpx.Response(200, json={"customers": [CUSTOMER_RESP]})
        )
        result = sync_client.customers.list()
        assert r19.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Customer)
        assert result[0].id == 10
        assert_store_id(r19)

        # Step 20: customers.update(10, data)
        r20 = respx.patch(f"{BASE_URL}/v1/customers/{CUSTOMER_ID}").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_UPDATED_RESP})
        )
        result = sync_client.customers.update(CUSTOMER_ID, CUSTOMER_UPDATE_DATA)
        assert r20.called
        body = json.loads(r20.calls.last.request.content)
        assert "customer" in body
        assert body["customer"]["name"] == "Joao Silva Atualizado"
        assert_store_id(r20)
        assert isinstance(result, Customer)
        assert result.name == "Joao Silva Atualizado"

        # Step 21: customers.find(cpf_cnpj=...)
        r21 = respx.get(f"{BASE_URL}/v1/customers/find").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = sync_client.customers.find(cpf_cnpj="12345678900")
        assert r21.called
        url = str(r21.calls.last.request.url)
        assert "cpf_cnpj=12345678900" in url
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r21)

        # =============================================================
        # Phase 6: Lead Management
        # =============================================================

        # Step 22: leads.create(data)
        r22 = respx.post(f"{BASE_URL}/v1/banks_api/leads").mock(
            return_value=httpx.Response(200, json={"data": LEAD_RESP})
        )
        result = sync_client.leads.create(LEAD_CREATE_DATA)
        assert r22.called
        body = json.loads(r22.calls.last.request.content)
        assert "lead" in body
        payload = body["lead"]
        assert payload["cpf_cnpj"] == "12345678900"
        assert payload["name"] == "Joao Silva"
        assert payload["birthdate"] == "1990-05-20"
        assert payload["email"] == "joao@example.com"
        assert payload["phone_number"] == "11999998888"
        assert payload["monthly_income"] == 600000
        assert_store_id(r22)
        assert isinstance(result, Lead)
        assert result.id == 1
        assert result.cpf_cnpj == "12345678900"

        # Step 23: leads.get(cpf)
        r23 = respx.get(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(200, json={"data": LEAD_RESP})
        )
        result = sync_client.leads.get(LEAD_CPF)
        assert r23.called
        assert isinstance(result, Lead)
        assert result.id == 1
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r23)

        # Step 24: leads.list()
        r24 = respx.get(f"{BASE_URL}/v1/banks_api/leads").mock(
            return_value=httpx.Response(200, json={"data": [LEAD_RESP]})
        )
        result = sync_client.leads.list()
        assert r24.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Lead)
        assert result[0].id == 1
        assert_store_id(r24)

        # Step 25: leads.update(cpf, data)
        r25 = respx.patch(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(200, json={"data": LEAD_UPDATED_RESP})
        )
        result = sync_client.leads.update(LEAD_CPF, LEAD_UPDATE_DATA)
        assert r25.called
        body = json.loads(r25.calls.last.request.content)
        assert "lead" in body
        assert body["lead"]["name"] == "Joao Atualizado"
        assert_store_id(r25)
        assert isinstance(result, Lead)
        assert result.name == "Joao Atualizado"

        # Step 26: leads.required_fields(cpf)
        r26 = respx.get(
            f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}/required_fields"
        ).mock(
            return_value=httpx.Response(200, json={"data": LEAD_REQUIRED_FIELDS_RESP})
        )
        result = sync_client.leads.required_fields(LEAD_CPF)
        assert r26.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None
        assert result.requirements is not None
        assert_store_id(r26)

        # =============================================================
        # Phase 7: Credit Simulation
        # =============================================================

        # Step 27: simulations.create(data)
        r27 = respx.post(f"{BASE_URL}/v1/banks_api/simulations").mock(
            return_value=httpx.Response(200, json={"data": SIMULATION_RESP})
        )
        result = sync_client.simulations.create(SIMULATION_CREATE_DATA)
        assert r27.called
        body = json.loads(r27.calls.last.request.content)
        sim = body["simulation"]
        assert sim["assets_value"] == 7000000
        assert sim["documentation_value"] == 50000
        assert sim["seller_cpf"] == "99988877766"
        assert sim["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(sim["conditions"]) == 1
        cond = sim["conditions"][0]
        assert cond["down_payment"] == 1500000
        assert cond["financed_amount"] == 5500000
        assert cond["installments"] == 48
        veh = sim["vehicle"]
        assert veh["asset_value"] == 7000000
        assert veh["licensing_uf"] == "SP"
        assert veh["manufacture_year"] == 2024
        assert veh["model_year"] == 2024
        assert veh["vehicle_molicar_code"] == "MOL456"
        assert veh["zero_km"] is True
        assert_store_id(r27)
        assert isinstance(result, Simulation)
        assert result.assets_value == 7000000
        assert result.conditions is not None
        assert len(result.conditions) == 1

        # Step 28: simulations.list()
        r28 = respx.get(f"{BASE_URL}/v1/proposal_simulations").mock(
            return_value=httpx.Response(200, json={"data": [SIMULATION_RESP]})
        )
        result = sync_client.simulations.list()
        assert r28.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Simulation)
        assert result[0].assets_value == 7000000
        assert_store_id(r28)

        # Step 29: simulations.get(uuid)
        r29 = respx.get(f"{BASE_URL}/v1/banks_api/simulations/{SIMULATION_UUID}").mock(
            return_value=httpx.Response(200, json={"data": SIMULATION_RESP})
        )
        result = sync_client.simulations.get(SIMULATION_UUID)
        assert r29.called
        assert isinstance(result, Simulation)
        assert result.assets_value == 7000000
        assert_store_id(r29)

        # =============================================================
        # Phase 8: Proposal Lifecycle
        # =============================================================

        # Step 30: proposals.create(data)
        r30 = respx.post(f"{BASE_URL}/v1/proposals").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = sync_client.proposals.create(PROPOSAL_CREATE_DATA)
        assert r30.called
        body = json.loads(r30.calls.last.request.content)
        prop = body["proposal"]
        assert prop["assets_value"] == 7000000
        assert prop["documentation_value"] == 50000
        assert prop["seller_cpf"] == "99988877766"
        assert prop["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(prop["conditions"]) == 1
        cond = prop["conditions"][0]
        assert cond["down_payment"] == 1500000
        assert cond["financed_amount"] == 5500000
        assert cond["installments"] == 48
        veh = prop["vehicle"]
        assert veh["asset_value"] == 7000000
        assert veh["licensing_uf"] == "SP"
        assert veh["manufacture_year"] == 2024
        assert veh["model_year"] == 2024
        assert veh["vehicle_molicar_code"] == "MOL456"
        assert veh["zero_km"] is True
        assert_store_id(r30)
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert result.assets_value == 7000000

        # Step 31: proposals.list()
        r31 = respx.get(f"{BASE_URL}/v1/proposals").mock(
            return_value=httpx.Response(200, json={"data": [PROPOSAL_RESP]})
        )
        result = sync_client.proposals.list()
        assert r31.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Proposal)
        assert result[0].id == PROPOSAL_ID
        assert_store_id(r31)

        # Step 32: proposals.get(id)
        r32 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = sync_client.proposals.get(PROPOSAL_ID)
        assert r32.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert result.assets_value == 7000000
        assert_store_id(r32)

        # Step 33: proposals.update(id, data)
        r33 = respx.put(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = sync_client.proposals.update(PROPOSAL_ID, PROPOSAL_CREATE_DATA)
        assert r33.called
        body = json.loads(r33.calls.last.request.content)
        assert "proposal" in body
        assert body["proposal"]["assets_value"] == 7000000
        assert_store_id(r33)
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID

        # Step 34: proposals.get_ownership(id)
        r34 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/get_ownership").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = sync_client.proposals.get_ownership(PROPOSAL_ID)
        assert r34.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert_store_id(r34)

        # Step 35: proposals.leave_ownership(id)
        r35 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/leave_ownership").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = sync_client.proposals.leave_ownership(PROPOSAL_ID)
        assert r35.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert_store_id(r35)

        # Step 36: proposals.activity_log(id)
        r36 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/activity_log").mock(
            return_value=httpx.Response(200, json={"data": ACTIVITY_LOG_RESP})
        )
        result = sync_client.proposals.activity_log(PROPOSAL_ID)
        assert r36.called
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["action"] == "created"
        assert_store_id(r36)

        # =============================================================
        # Phase 9: Proposal Attempts
        # =============================================================

        # Step 37: proposal_attempts.create(prop_id, data)
        r37 = respx.post(PA_URL).mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = sync_client.proposal_attempts.create(PROPOSAL_ID, ATTEMPT_CREATE_DATA)
        assert r37.called
        body = json.loads(r37.calls.last.request.content)
        assert isinstance(body, dict)
        assert_store_id(r37)
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1

        # Step 38: proposal_attempts.list(prop_id)
        r38 = respx.get(PA_URL).mock(
            return_value=httpx.Response(200, json={"data": [ATTEMPT_RESP]})
        )
        result = sync_client.proposal_attempts.list(PROPOSAL_ID)
        assert r38.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProposalAttempt)
        assert result[0].id == 1
        assert_store_id(r38)

        # Step 39: proposal_attempts.get(prop_id, att_id)
        r39 = respx.get(f"{PA_URL}/{ATTEMPT_ID}").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = sync_client.proposal_attempts.get(PROPOSAL_ID, ATTEMPT_ID)
        assert r39.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1
        assert_store_id(r39)

        # Step 40: proposal_attempts.update(prop_id, att_id, data)
        r40 = respx.put(f"{PA_URL}/{ATTEMPT_ID}").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = sync_client.proposal_attempts.update(
            PROPOSAL_ID, ATTEMPT_ID, ATTEMPT_UPDATE_DATA
        )
        assert r40.called
        body = json.loads(r40.calls.last.request.content)
        assert isinstance(body, dict)
        assert_store_id(r40)
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1

        # Step 41: proposal_attempts.perform_action(..., "approve")
        r41 = respx.get(f"{PA_URL}/{ATTEMPT_ID}/approve").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = sync_client.proposal_attempts.perform_action(
            PROPOSAL_ID, ATTEMPT_ID, "approve"
        )
        assert r41.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1
        assert_store_id(r41)

        # =============================================================
        # Phase 10: Inventory
        # =============================================================

        # Step 42: stock.create(data)
        r42 = respx.post(f"{BASE_URL}/v1/vehicles").mock(
            return_value=httpx.Response(200, json={"vehicle": STOCK_VEHICLE_RESP})
        )
        result = sync_client.stock.create(STOCK_CREATE_DATA)
        assert r42.called
        body = json.loads(r42.calls.last.request.content)
        assert "vehicle" in body
        payload = body["vehicle"]
        assert payload["vehicle_model_id"] == 300
        assert payload["store_id"] == 1
        assert payload["price_cents"] == 7000000
        assert payload["description"] == "Fiat Argo 1.0 2024"
        assert_store_id(r42)
        assert isinstance(result, StockVehicle)
        assert result.id == STOCK_VEHICLE_ID
        assert result.price_cents == 7000000

        # Step 43: stock.list()
        r43 = respx.get(f"{BASE_URL}/v1/vehicles").mock(
            return_value=httpx.Response(200, json=[STOCK_VEHICLE_RESP])
        )
        result = sync_client.stock.list()
        assert r43.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], StockVehicle)
        assert result[0].id == STOCK_VEHICLE_ID
        assert_store_id(r43)

        # Step 44: stock.update(id, data)
        r44 = respx.put(f"{BASE_URL}/v1/vehicles/{STOCK_VEHICLE_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle": STOCK_VEHICLE_UPDATED_RESP},
            )
        )
        result = sync_client.stock.update(STOCK_VEHICLE_ID, STOCK_UPDATE_DATA)
        assert r44.called
        body = json.loads(r44.calls.last.request.content)
        assert "vehicle" in body
        assert body["vehicle"]["price_cents"] == 7500000
        assert_store_id(r44)
        assert isinstance(result, StockVehicle)
        assert result.price_cents == 7500000

        # Step 45: stock.remove(id)
        r45 = respx.put(
            f"{BASE_URL}/v1/vehicles/{STOCK_VEHICLE_ID}/remove_from_stock"
        ).mock(return_value=httpx.Response(200, json={"vehicle": STOCK_VEHICLE_RESP}))
        result = sync_client.stock.remove(STOCK_VEHICLE_ID)
        assert r45.called
        assert isinstance(result, StockVehicle)
        assert result.id == STOCK_VEHICLE_ID
        assert_store_id(r45)

        # =============================================================
        # Phase 11: Plus Returns
        # =============================================================

        # Step 46: plus_returns.create(data)
        r46 = respx.post(f"{BASE_URL}/v1/plus_return_rules").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = sync_client.plus_returns.create(PLUS_RETURN_CREATE_DATA)
        assert r46.called
        body = json.loads(r46.calls.last.request.content)
        assert "plus_return_rule" in body
        assert isinstance(body["plus_return_rule"], dict)
        assert_store_id(r46)
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID

        # Step 47: plus_returns.list()
        r47 = respx.get(f"{BASE_URL}/v1/plus_return_rules").mock(
            return_value=httpx.Response(200, json=[PLUS_RETURN_RESP])
        )
        result = sync_client.plus_returns.list()
        assert r47.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], PlusReturnRule)
        assert result[0].id == PLUS_RETURN_ID
        assert_store_id(r47)

        # Step 48: plus_returns.get(id)
        r48 = respx.get(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = sync_client.plus_returns.get(PLUS_RETURN_ID)
        assert r48.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r48)

        # Step 49: plus_returns.update(id, data)
        r49 = respx.patch(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = sync_client.plus_returns.update(
            PLUS_RETURN_ID, PLUS_RETURN_UPDATE_DATA
        )
        assert r49.called
        body = json.loads(r49.calls.last.request.content)
        assert "plus_return_rule" in body
        assert isinstance(body["plus_return_rule"], dict)
        assert_store_id(r49)
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID

        # Step 50: plus_returns.activate(id)
        r50 = respx.get(
            f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}/activate"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = sync_client.plus_returns.activate(PLUS_RETURN_ID)
        assert r50.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r50)

        # Step 51: plus_returns.deactivate(id)
        r51 = respx.get(
            f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}/deactivate"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = sync_client.plus_returns.deactivate(PLUS_RETURN_ID)
        assert r51.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r51)

        # Step 52: plus_returns.delete(id)
        r52 = respx.delete(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(204)
        )
        result = sync_client.plus_returns.delete(PLUS_RETURN_ID)
        assert r52.called
        assert result is None
        assert_store_id(r52)

        # =============================================================
        # Phase 12: Cleanup
        # =============================================================

        # Step 53: leads.delete(cpf)
        r53 = respx.delete(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(204)
        )
        result = sync_client.leads.delete(LEAD_CPF)
        assert r53.called
        assert result is None
        assert_store_id(r53)

        # Step 54: proposals.delete(id)
        r54 = respx.delete(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(204)
        )
        result = sync_client.proposals.delete(PROPOSAL_ID)
        assert r54.called
        assert result is None
        assert_store_id(r54)

    # ===================================================================
    # Async variant — same flow with await
    # ===================================================================

    @respx.mock
    async def test_async_full_workflow(self, async_client: AsyncCredereClient) -> None:
        # =============================================================
        # Phase 1: Auth & User Context
        # =============================================================

        # Step 1: users.current()
        r1 = respx.get(f"{BASE_URL}/v1/users/current").mock(
            return_value=httpx.Response(200, json={"user": USER_RESP})
        )
        result = await async_client.users.current()
        assert r1.called
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "Admin"
        assert "Store-Id" not in r1.calls.last.request.headers

        # Step 2: users.proposals_filter_list()
        r2 = respx.get(f"{BASE_URL}/v1/users/proposals_filter_list").mock(
            return_value=httpx.Response(200, json={"users": [USER_RESP]})
        )
        result = await async_client.users.proposals_filter_list()
        assert r2.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], User)
        assert result[0].id == 1
        assert result[0].name == "Admin"
        assert_store_id(r2)

        # =============================================================
        # Phase 2: Store Setup
        # =============================================================

        # Step 3: stores.create()
        r3 = respx.post(f"{BASE_URL}/v1/stores").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = await async_client.stores.create(STORE_CREATE_DATA)
        assert r3.called
        body = json.loads(r3.calls.last.request.content)
        assert "store" in body
        assert body["store"]["name"] == "Loja Central"
        assert body["store"]["display_name"] == "Central"
        assert body["store"]["cnpj"] == "11222333000181"
        assert_store_id(r3)
        assert isinstance(result, Store)
        assert result.id == 1
        assert result.name == "Loja Central"

        # Step 4: stores.list()
        r4 = respx.get(f"{BASE_URL}/v1/stores").mock(
            return_value=httpx.Response(200, json={"stores": [STORE_RESP]})
        )
        result = await async_client.stores.list()
        assert r4.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Store)
        assert result[0].id == 1
        assert_store_id(r4)

        # Step 5: stores.activate(1)
        r5 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/activate").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = await async_client.stores.activate(STORE_ID)
        assert r5.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert_store_id(r5)

        # Step 6: stores.deactivate(1)
        r6 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/deactivate").mock(
            return_value=httpx.Response(200, json={"store": STORE_RESP})
        )
        result = await async_client.stores.deactivate(STORE_ID)
        assert r6.called
        assert isinstance(result, Store)
        assert result.id == 1
        assert_store_id(r6)

        # =============================================================
        # Phase 3: Reference Data
        # =============================================================

        # Step 7: utilities.domains()
        r7 = respx.get(f"{BASE_URL}/v1/domains").mock(
            return_value=httpx.Response(200, json=[DOMAIN_RESP])
        )
        result = await async_client.utilities.domains()
        assert r7.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert result[0].label == "Masculino"
        assert_store_id(r7)

        # Step 8: utilities.lead_domains()
        r8 = respx.get(f"{BASE_URL}/v1/banks_api/domains").mock(
            return_value=httpx.Response(200, json=[DOMAIN_RESP])
        )
        result = await async_client.utilities.lead_domains()
        assert r8.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert_store_id(r8)

        # Step 9: utilities.banks()
        r9 = respx.get(f"{BASE_URL}/v1/banks").mock(
            return_value=httpx.Response(200, json={"banks": [BANK_RESP]})
        )
        result = await async_client.utilities.banks()
        assert r9.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Bank)
        assert result[0].id == 1
        assert result[0].name == "Banco do Brasil"
        assert_store_id(r9)

        # Step 10: utilities.vehicle_by_plate("ABC1D23")
        r10 = respx.get(f"{BASE_URL}/v1/vehicles/license_plate/ABC1D23").mock(
            return_value=httpx.Response(200, json=VEHICLE_BY_PLATE_RESP)
        )
        result = await async_client.utilities.vehicle_by_plate("ABC1D23")
        assert r10.called
        assert isinstance(result, dict)
        assert result["plate"] == "ABC1D23"
        assert result["brand"] == "Fiat"
        assert_store_id(r10)

        # Step 11: utilities.vehicle_by_chassis(...)
        r11 = respx.get(f"{BASE_URL}/v1/vehicles/chassi_code/{CHASSI_CODE}").mock(
            return_value=httpx.Response(200, json=VEHICLE_BY_CHASSI_RESP)
        )
        result = await async_client.utilities.vehicle_by_chassis(CHASSI_CODE)
        assert r11.called
        assert isinstance(result, dict)
        assert result["chassi"] == CHASSI_CODE
        assert result["brand"] == "Fiat"
        assert_store_id(r11)

        # Step 12: vehicle_models.list()
        r12 = respx.get(f"{BASE_URL}/v1/vehicle_models").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_models": [VEHICLE_MODEL_RESP]},
            )
        )
        result = await async_client.vehicle_models.list()
        assert r12.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehicleModel)
        assert result[0].id == VEHICLE_MODEL_ID
        assert result[0].name == "Argo 1.0"
        assert_store_id(r12)

        # Step 13: vehicle_models.search("Argo")
        r13 = respx.get(f"{BASE_URL}/v1/vehicle_models/search").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_model": VEHICLE_MODEL_RESP},
            )
        )
        result = await async_client.vehicle_models.search("Argo")
        assert r13.called
        assert isinstance(result, VehicleModel)
        assert result.molicar_code == "MOL456"
        assert result.id == VEHICLE_MODEL_ID
        assert_store_id(r13)

        # Step 14: vehicle_models.prices()
        r14 = respx.get(f"{BASE_URL}/v1/vehicle_prices").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle_prices": [VEHICLE_PRICE_RESP]},
            )
        )
        result = await async_client.vehicle_models.prices()
        assert r14.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], VehiclePrice)
        assert result[0].id == 1
        assert result[0].default_price_cents == 7000000
        assert_store_id(r14)

        # =============================================================
        # Phase 4: Bank Integration
        # =============================================================

        # Step 15: bank_credentials.persist(1)
        r15 = respx.get(
            f"{BASE_URL}/v1/stores/{STORE_ID}/persist_cnpj_bank_credentials"
        ).mock(return_value=httpx.Response(200, json=BANK_PERSIST_RESP))
        result = await async_client.bank_credentials.persist(STORE_ID)
        assert r15.called
        assert isinstance(result, dict)
        assert result["persisted"] is True
        assert_store_id(r15)

        # Step 16: bank_credentials.list(1)
        r16 = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/integrated_banks").mock(
            return_value=httpx.Response(
                200,
                json={"integrated_banks": [INTEGRATED_BANK_RESP]},
            )
        )
        result = await async_client.bank_credentials.list(store_id=STORE_ID)
        assert r16.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], IntegratedBank)
        assert result[0].id == 1
        assert result[0].credentials_status == "active"
        assert_store_id(r16)

        # =============================================================
        # Phase 5: Customer Management
        # =============================================================

        # Step 17: customers.create(data)
        r17 = respx.post(f"{BASE_URL}/v1/customers").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = await async_client.customers.create(CUSTOMER_CREATE_DATA)
        assert r17.called
        body = json.loads(r17.calls.last.request.content)
        assert "customer" in body
        payload = body["customer"]
        assert payload["cpf_cnpj"] == "12345678900"
        assert payload["name"] == "Joao Silva"
        assert payload["birthdate"] == "1990-05-20"
        assert payload["email"] == "joao@example.com"
        assert payload["phone_number"] == "11999998888"
        assert payload["monthly_income"] == 600000
        assert_store_id(r17)
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert result.name == "Joao Silva"

        # Step 18: customers.get(10)
        r18 = respx.get(f"{BASE_URL}/v1/customers/{CUSTOMER_ID}").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = await async_client.customers.get(CUSTOMER_ID)
        assert r18.called
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r18)

        # Step 19: customers.list()
        r19 = respx.get(f"{BASE_URL}/v1/customers").mock(
            return_value=httpx.Response(200, json={"customers": [CUSTOMER_RESP]})
        )
        result = await async_client.customers.list()
        assert r19.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Customer)
        assert result[0].id == 10
        assert_store_id(r19)

        # Step 20: customers.update(10, data)
        r20 = respx.patch(f"{BASE_URL}/v1/customers/{CUSTOMER_ID}").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_UPDATED_RESP})
        )
        result = await async_client.customers.update(CUSTOMER_ID, CUSTOMER_UPDATE_DATA)
        assert r20.called
        body = json.loads(r20.calls.last.request.content)
        assert "customer" in body
        assert body["customer"]["name"] == "Joao Silva Atualizado"
        assert_store_id(r20)
        assert isinstance(result, Customer)
        assert result.name == "Joao Silva Atualizado"

        # Step 21: customers.find(cpf_cnpj=...)
        r21 = respx.get(f"{BASE_URL}/v1/customers/find").mock(
            return_value=httpx.Response(200, json={"customer": CUSTOMER_RESP})
        )
        result = await async_client.customers.find(cpf_cnpj="12345678900")
        assert r21.called
        url = str(r21.calls.last.request.url)
        assert "cpf_cnpj=12345678900" in url
        assert isinstance(result, Customer)
        assert result.id == 10
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r21)

        # =============================================================
        # Phase 6: Lead Management
        # =============================================================

        # Step 22: leads.create(data)
        r22 = respx.post(f"{BASE_URL}/v1/banks_api/leads").mock(
            return_value=httpx.Response(200, json={"data": LEAD_RESP})
        )
        result = await async_client.leads.create(LEAD_CREATE_DATA)
        assert r22.called
        body = json.loads(r22.calls.last.request.content)
        assert "lead" in body
        payload = body["lead"]
        assert payload["cpf_cnpj"] == "12345678900"
        assert payload["name"] == "Joao Silva"
        assert payload["birthdate"] == "1990-05-20"
        assert payload["email"] == "joao@example.com"
        assert payload["phone_number"] == "11999998888"
        assert payload["monthly_income"] == 600000
        assert_store_id(r22)
        assert isinstance(result, Lead)
        assert result.id == 1
        assert result.cpf_cnpj == "12345678900"

        # Step 23: leads.get(cpf)
        r23 = respx.get(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(200, json={"data": LEAD_RESP})
        )
        result = await async_client.leads.get(LEAD_CPF)
        assert r23.called
        assert isinstance(result, Lead)
        assert result.id == 1
        assert result.cpf_cnpj == "12345678900"
        assert_store_id(r23)

        # Step 24: leads.list()
        r24 = respx.get(f"{BASE_URL}/v1/banks_api/leads").mock(
            return_value=httpx.Response(200, json={"data": [LEAD_RESP]})
        )
        result = await async_client.leads.list()
        assert r24.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Lead)
        assert result[0].id == 1
        assert_store_id(r24)

        # Step 25: leads.update(cpf, data)
        r25 = respx.patch(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(200, json={"data": LEAD_UPDATED_RESP})
        )
        result = await async_client.leads.update(LEAD_CPF, LEAD_UPDATE_DATA)
        assert r25.called
        body = json.loads(r25.calls.last.request.content)
        assert "lead" in body
        assert body["lead"]["name"] == "Joao Atualizado"
        assert_store_id(r25)
        assert isinstance(result, Lead)
        assert result.name == "Joao Atualizado"

        # Step 26: leads.required_fields(cpf)
        r26 = respx.get(
            f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}/required_fields"
        ).mock(
            return_value=httpx.Response(200, json={"data": LEAD_REQUIRED_FIELDS_RESP})
        )
        result = await async_client.leads.required_fields(LEAD_CPF)
        assert r26.called
        assert isinstance(result, LeadRequiredFields)
        assert result.lead is not None
        assert result.requirements is not None
        assert_store_id(r26)

        # =============================================================
        # Phase 7: Credit Simulation
        # =============================================================

        # Step 27: simulations.create(data)
        r27 = respx.post(f"{BASE_URL}/v1/banks_api/simulations").mock(
            return_value=httpx.Response(200, json={"data": SIMULATION_RESP})
        )
        result = await async_client.simulations.create(SIMULATION_CREATE_DATA)
        assert r27.called
        body = json.loads(r27.calls.last.request.content)
        sim = body["simulation"]
        assert sim["assets_value"] == 7000000
        assert sim["documentation_value"] == 50000
        assert sim["seller_cpf"] == "99988877766"
        assert sim["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(sim["conditions"]) == 1
        cond = sim["conditions"][0]
        assert cond["down_payment"] == 1500000
        assert cond["financed_amount"] == 5500000
        assert cond["installments"] == 48
        veh = sim["vehicle"]
        assert veh["asset_value"] == 7000000
        assert veh["licensing_uf"] == "SP"
        assert veh["manufacture_year"] == 2024
        assert veh["model_year"] == 2024
        assert veh["vehicle_molicar_code"] == "MOL456"
        assert veh["zero_km"] is True
        assert_store_id(r27)
        assert isinstance(result, Simulation)
        assert result.assets_value == 7000000
        assert result.conditions is not None
        assert len(result.conditions) == 1

        # Step 28: simulations.list()
        r28 = respx.get(f"{BASE_URL}/v1/proposal_simulations").mock(
            return_value=httpx.Response(200, json={"data": [SIMULATION_RESP]})
        )
        result = await async_client.simulations.list()
        assert r28.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Simulation)
        assert result[0].assets_value == 7000000
        assert_store_id(r28)

        # Step 29: simulations.get(uuid)
        r29 = respx.get(f"{BASE_URL}/v1/banks_api/simulations/{SIMULATION_UUID}").mock(
            return_value=httpx.Response(200, json={"data": SIMULATION_RESP})
        )
        result = await async_client.simulations.get(SIMULATION_UUID)
        assert r29.called
        assert isinstance(result, Simulation)
        assert result.assets_value == 7000000
        assert_store_id(r29)

        # =============================================================
        # Phase 8: Proposal Lifecycle
        # =============================================================

        # Step 30: proposals.create(data)
        r30 = respx.post(f"{BASE_URL}/v1/proposals").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = await async_client.proposals.create(PROPOSAL_CREATE_DATA)
        assert r30.called
        body = json.loads(r30.calls.last.request.content)
        prop = body["proposal"]
        assert prop["assets_value"] == 7000000
        assert prop["documentation_value"] == 50000
        assert prop["seller_cpf"] == "99988877766"
        assert prop["retrieve_lead"]["cpf_cnpj"] == "12345678900"
        assert len(prop["conditions"]) == 1
        cond = prop["conditions"][0]
        assert cond["down_payment"] == 1500000
        assert cond["financed_amount"] == 5500000
        assert cond["installments"] == 48
        veh = prop["vehicle"]
        assert veh["asset_value"] == 7000000
        assert veh["licensing_uf"] == "SP"
        assert veh["manufacture_year"] == 2024
        assert veh["model_year"] == 2024
        assert veh["vehicle_molicar_code"] == "MOL456"
        assert veh["zero_km"] is True
        assert_store_id(r30)
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert result.assets_value == 7000000

        # Step 31: proposals.list()
        r31 = respx.get(f"{BASE_URL}/v1/proposals").mock(
            return_value=httpx.Response(200, json={"data": [PROPOSAL_RESP]})
        )
        result = await async_client.proposals.list()
        assert r31.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Proposal)
        assert result[0].id == PROPOSAL_ID
        assert_store_id(r31)

        # Step 32: proposals.get(id)
        r32 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = await async_client.proposals.get(PROPOSAL_ID)
        assert r32.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert result.assets_value == 7000000
        assert_store_id(r32)

        # Step 33: proposals.update(id, data)
        r33 = respx.put(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = await async_client.proposals.update(PROPOSAL_ID, PROPOSAL_CREATE_DATA)
        assert r33.called
        body = json.loads(r33.calls.last.request.content)
        assert "proposal" in body
        assert body["proposal"]["assets_value"] == 7000000
        assert_store_id(r33)
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID

        # Step 34: proposals.get_ownership(id)
        r34 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/get_ownership").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = await async_client.proposals.get_ownership(PROPOSAL_ID)
        assert r34.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert_store_id(r34)

        # Step 35: proposals.leave_ownership(id)
        r35 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/leave_ownership").mock(
            return_value=httpx.Response(200, json={"data": PROPOSAL_RESP})
        )
        result = await async_client.proposals.leave_ownership(PROPOSAL_ID)
        assert r35.called
        assert isinstance(result, Proposal)
        assert result.id == PROPOSAL_ID
        assert_store_id(r35)

        # Step 36: proposals.activity_log(id)
        r36 = respx.get(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}/activity_log").mock(
            return_value=httpx.Response(200, json={"data": ACTIVITY_LOG_RESP})
        )
        result = await async_client.proposals.activity_log(PROPOSAL_ID)
        assert r36.called
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["action"] == "created"
        assert_store_id(r36)

        # =============================================================
        # Phase 9: Proposal Attempts
        # =============================================================

        # Step 37: proposal_attempts.create(prop_id, data)
        r37 = respx.post(PA_URL).mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = await async_client.proposal_attempts.create(
            PROPOSAL_ID, ATTEMPT_CREATE_DATA
        )
        assert r37.called
        body = json.loads(r37.calls.last.request.content)
        assert isinstance(body, dict)
        assert_store_id(r37)
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1

        # Step 38: proposal_attempts.list(prop_id)
        r38 = respx.get(PA_URL).mock(
            return_value=httpx.Response(200, json={"data": [ATTEMPT_RESP]})
        )
        result = await async_client.proposal_attempts.list(PROPOSAL_ID)
        assert r38.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProposalAttempt)
        assert result[0].id == 1
        assert_store_id(r38)

        # Step 39: proposal_attempts.get(prop_id, att_id)
        r39 = respx.get(f"{PA_URL}/{ATTEMPT_ID}").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = await async_client.proposal_attempts.get(PROPOSAL_ID, ATTEMPT_ID)
        assert r39.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1
        assert_store_id(r39)

        # Step 40: proposal_attempts.update(prop_id, att_id, data)
        r40 = respx.put(f"{PA_URL}/{ATTEMPT_ID}").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = await async_client.proposal_attempts.update(
            PROPOSAL_ID, ATTEMPT_ID, ATTEMPT_UPDATE_DATA
        )
        assert r40.called
        body = json.loads(r40.calls.last.request.content)
        assert isinstance(body, dict)
        assert_store_id(r40)
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1

        # Step 41: proposal_attempts.perform_action(..., "approve")
        r41 = respx.get(f"{PA_URL}/{ATTEMPT_ID}/approve").mock(
            return_value=httpx.Response(200, json={"data": ATTEMPT_RESP})
        )
        result = await async_client.proposal_attempts.perform_action(
            PROPOSAL_ID, ATTEMPT_ID, "approve"
        )
        assert r41.called
        assert isinstance(result, ProposalAttempt)
        assert result.id == 1
        assert_store_id(r41)

        # =============================================================
        # Phase 10: Inventory
        # =============================================================

        # Step 42: stock.create(data)
        r42 = respx.post(f"{BASE_URL}/v1/vehicles").mock(
            return_value=httpx.Response(200, json={"vehicle": STOCK_VEHICLE_RESP})
        )
        result = await async_client.stock.create(STOCK_CREATE_DATA)
        assert r42.called
        body = json.loads(r42.calls.last.request.content)
        assert "vehicle" in body
        payload = body["vehicle"]
        assert payload["vehicle_model_id"] == 300
        assert payload["store_id"] == 1
        assert payload["price_cents"] == 7000000
        assert payload["description"] == "Fiat Argo 1.0 2024"
        assert_store_id(r42)
        assert isinstance(result, StockVehicle)
        assert result.id == STOCK_VEHICLE_ID
        assert result.price_cents == 7000000

        # Step 43: stock.list()
        r43 = respx.get(f"{BASE_URL}/v1/vehicles").mock(
            return_value=httpx.Response(200, json=[STOCK_VEHICLE_RESP])
        )
        result = await async_client.stock.list()
        assert r43.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], StockVehicle)
        assert result[0].id == STOCK_VEHICLE_ID
        assert_store_id(r43)

        # Step 44: stock.update(id, data)
        r44 = respx.put(f"{BASE_URL}/v1/vehicles/{STOCK_VEHICLE_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"vehicle": STOCK_VEHICLE_UPDATED_RESP},
            )
        )
        result = await async_client.stock.update(STOCK_VEHICLE_ID, STOCK_UPDATE_DATA)
        assert r44.called
        body = json.loads(r44.calls.last.request.content)
        assert "vehicle" in body
        assert body["vehicle"]["price_cents"] == 7500000
        assert_store_id(r44)
        assert isinstance(result, StockVehicle)
        assert result.price_cents == 7500000

        # Step 45: stock.remove(id)
        r45 = respx.put(
            f"{BASE_URL}/v1/vehicles/{STOCK_VEHICLE_ID}/remove_from_stock"
        ).mock(return_value=httpx.Response(200, json={"vehicle": STOCK_VEHICLE_RESP}))
        result = await async_client.stock.remove(STOCK_VEHICLE_ID)
        assert r45.called
        assert isinstance(result, StockVehicle)
        assert result.id == STOCK_VEHICLE_ID
        assert_store_id(r45)

        # =============================================================
        # Phase 11: Plus Returns
        # =============================================================

        # Step 46: plus_returns.create(data)
        r46 = respx.post(f"{BASE_URL}/v1/plus_return_rules").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = await async_client.plus_returns.create(PLUS_RETURN_CREATE_DATA)
        assert r46.called
        body = json.loads(r46.calls.last.request.content)
        assert "plus_return_rule" in body
        assert isinstance(body["plus_return_rule"], dict)
        assert_store_id(r46)
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID

        # Step 47: plus_returns.list()
        r47 = respx.get(f"{BASE_URL}/v1/plus_return_rules").mock(
            return_value=httpx.Response(200, json=[PLUS_RETURN_RESP])
        )
        result = await async_client.plus_returns.list()
        assert r47.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], PlusReturnRule)
        assert result[0].id == PLUS_RETURN_ID
        assert_store_id(r47)

        # Step 48: plus_returns.get(id)
        r48 = respx.get(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = await async_client.plus_returns.get(PLUS_RETURN_ID)
        assert r48.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r48)

        # Step 49: plus_returns.update(id, data)
        r49 = respx.patch(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = await async_client.plus_returns.update(
            PLUS_RETURN_ID, PLUS_RETURN_UPDATE_DATA
        )
        assert r49.called
        body = json.loads(r49.calls.last.request.content)
        assert "plus_return_rule" in body
        assert isinstance(body["plus_return_rule"], dict)
        assert_store_id(r49)
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID

        # Step 50: plus_returns.activate(id)
        r50 = respx.get(
            f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}/activate"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = await async_client.plus_returns.activate(PLUS_RETURN_ID)
        assert r50.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r50)

        # Step 51: plus_returns.deactivate(id)
        r51 = respx.get(
            f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}/deactivate"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"plus_return_rule": PLUS_RETURN_RESP},
            )
        )
        result = await async_client.plus_returns.deactivate(PLUS_RETURN_ID)
        assert r51.called
        assert isinstance(result, PlusReturnRule)
        assert result.id == PLUS_RETURN_ID
        assert_store_id(r51)

        # Step 52: plus_returns.delete(id)
        r52 = respx.delete(f"{BASE_URL}/v1/plus_return_rules/{PLUS_RETURN_ID}").mock(
            return_value=httpx.Response(204)
        )
        result = await async_client.plus_returns.delete(PLUS_RETURN_ID)
        assert r52.called
        assert result is None
        assert_store_id(r52)

        # =============================================================
        # Phase 12: Cleanup
        # =============================================================

        # Step 53: leads.delete(cpf)
        r53 = respx.delete(f"{BASE_URL}/v1/banks_api/leads/{LEAD_CPF}").mock(
            return_value=httpx.Response(204)
        )
        result = await async_client.leads.delete(LEAD_CPF)
        assert r53.called
        assert result is None
        assert_store_id(r53)

        # Step 54: proposals.delete(id)
        r54 = respx.delete(f"{BASE_URL}/v1/proposals/{PROPOSAL_ID}").mock(
            return_value=httpx.Response(204)
        )
        result = await async_client.proposals.delete(PROPOSAL_ID)
        assert r54.called
        assert result is None
        assert_store_id(r54)
