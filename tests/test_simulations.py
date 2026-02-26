"""Tests for the Simulations resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError, NotFoundError
from credere.models.simulations import SimulationData, SimulationResponse

BASE_URL = "https://api.credere.com"
SIMULATIONS_URL = f"{BASE_URL}/v1/banks_api/simulations"
LIST_URL = f"{BASE_URL}/v1/proposal_simulations"

SAMPLE_SIMULATION_CREATE_DATA = {
    "simulation": {
        "process_bank_suggested_conditions": True,
        "process_credere_suggested_conditions": False,
        "seller_cpf": "00000000000",
        "retrieve_lead": {"cpf_cnpj": "000.000.000-00"},
        "bank_febraban_codes": [
            "M22",
            "623",
            "422",
            "033",
            "655",
            "341",
            "342",
            "fontecred",
            "moneyplus",
        ],
        "documentation_value": 100000,
        "accessory_value": 100000,
        "insurance_value": 100000,
        "commercial": False,
        "vehicle": {
            "credere_vehicle_model_id": "0000",
            "licensing_uf": "SP",
            "licensing_city": "São Paulo",
            "manufacture_year": 2022,
            "model_year": 2022,
            "asset_value": 10000000,
            "zero_km": True,
        },
        "conditions": [
            {"installments": 12, "down_payment": 1000000},
            {"installments": 24, "down_payment": 1000000, "bank_febraban_code": "M22"},
            {
                "installments": 36,
                "down_payment": 1000000,
                "products_options": {
                    "include_capitalization_bond": True,
                    "include_asset_insurance": True,
                },
                "include_financial_protection_insurance": True,
                "process_credere_suggested_conditions": False,
            },
            {
                "installments": 48,
                "down_payment": 1000000,
                "max_return": "0",
                "min_return": "5",
                "return_preference": "max",
                "quota_preference": "min",
            },
        ],
    }
}

SAMPLE_SIMULATION_RESPONSE = {
    "data": {
        "assets_value": 3499900,
        "conditions": [
            {
                "financed_amount": 2121262,
                "amount_paid_in_financing": 2883816,
                "bank_down_payment_suggestion": 1749950,
                "process_condition_payload": {
                    "simulation_token": "ca1235a3-ac1b-3e28-b1c3-dcf926a13a61",
                    "tab_id": 123,
                    "tab_uuid": "ca1235a3-ac1b-3e28-b1c3-dcf926a13a61",
                },
                "bank": {
                    "febraban_code": "033",
                    "id": 123,
                    "name": "Banco Santander (Brasil) S.A.",
                    "nickname": "Santander",
                },
                "reason": None,
                "run_pre_approval": True,
                "pre_approval_status": 3,
                "return_preference": "max",
                "expenses": [
                    {
                        "fixed_value": 18751,
                        "id": 123,
                        "max_value": 18751,
                        "min_value": 18751,
                        "over_total": False,
                        "payload": {
                            "bank_expense_id": None,
                            "credere_type": "contract_record_rate",
                        },
                        "percentage": 0,
                        "type": "contract_record_rate",
                        "value": 18751,
                    },
                    {
                        "fixed_value": 29500,
                        "id": 456,
                        "max_value": 29500,
                        "min_value": 29500,
                        "over_total": False,
                        "payload": {
                            "bank_expense_id": None,
                            "credere_type": "property_valuation_rate",
                        },
                        "percentage": 0,
                        "type": "property_valuation_rate",
                        "value": 29500,
                    },
                    {
                        "fixed_value": 170208,
                        "id": 789,
                        "max_value": 170208,
                        "min_value": 170208,
                        "over_total": False,
                        "payload": {"bank_expense_id": "86", "credere_type": "spf"},
                        "percentage": 0,
                        "type": "spf",
                        "value": 170208,
                    },
                    {
                        "fixed_value": 93000,
                        "id": 321,
                        "max_value": 93000,
                        "min_value": 93000,
                        "over_total": False,
                        "payload": {
                            "bank_expense_id": None,
                            "credere_type": "register_rate",
                        },
                        "percentage": 0,
                        "type": "register_rate",
                        "value": 93000,
                    },
                    {
                        "fixed_value": 59853,
                        "id": 654,
                        "max_value": 59853,
                        "min_value": 59853,
                        "over_total": False,
                        "payload": {
                            "bank_expense_id": None,
                            "credere_type": "iof_value",
                        },
                        "percentage": 0,
                        "type": "iof_value",
                        "value": 59853,
                    },
                ],
                "last_installment_value": 120159,
                "interest_annually": 36.37,
                "process_task": {
                    "ended_at": "2022-03-06T19:18:43Z",
                    "error": False,
                    "result": {"success": True},
                },
                "success": True,
                "include_financial_protection_insurance": True,
                "error": False,
                "pre_aproval_task": None,
                "quota_preference": "min",
                "first_installment_value": 120159,
                "min_return": 0,
                "max_return": 6,
                "id": 123,
                "available": True,
                "down_payment": 1749950,
                "installments": 24,
                "payment_flow": {
                    "1": 120159,
                    "2": 120159,
                    "3": 120159,
                    "4": 120159,
                    "5": 120159,
                    "6": 120159,
                    "7": 120159,
                    "8": 120159,
                    "9": 120159,
                    "10": 120159,
                    "11": 120159,
                    "12": 120159,
                    "13": 120159,
                    "14": 120159,
                    "15": 120159,
                    "16": 120159,
                    "17": 120159,
                    "18": 120159,
                    "19": 120159,
                    "20": 120159,
                    "21": 120159,
                    "22": 120159,
                    "23": 120159,
                    "24": 120159,
                },
                "cet_annually": 69.9,
                "reason_identifier": None,
                "fixed_installments": True,
                "credit_condition_description": None,
                "bank_available_amount": None,
                "credit_condition_code": "87816",
                "products_options": {
                    "include_asset_insurance": False,
                    "include_capitalization_bond": False,
                },
                "suggestion_reason": "bank_suggested_down_payment",
                "created_at": "2022-03-06T19:18:42Z",
                "cet_monthly": 4.45,
                "bank_minimum_down_payment": 1749950,
                "processed_at": "2022-03-06T19:18:43Z",
                "credit_condition_return": "3",
                "interest_monthly": 2.62,
            }
        ],
        "created_at": "2022-03-06T19:18:36Z",
        "error": None,
        "items": [{"id": 123, "type": "documentation", "value": 0}],
        "lead": {
            "address": {
                "city": None,
                "complement": None,
                "district": None,
                "id": 123,
                "number": None,
                "state": None,
                "street": None,
                "zip_code": None,
            },
            "birthdate": "1991-01-01",
            "cpf_cnpj": "000.000.000-00",
            "email": "fulano@example.com",
            "gender": {
                "credere_identifier": "M",
                "id": 123,
                "label": "Masculino",
                "type": "gender",
            },
            "has_cnh": True,
            "id": 123,
            "monthly_income": None,
            "mother_name": None,
            "name": "Fulano dos Santos",
            "occupation": None,
            "payload": {},
            "phone_number": "+5511987654321",
            "profession": None,
        },
        "payload": {"application_id": 1},
        "process_bank_suggested_conditions": True,
        "process_task": {
            "ended_at": "2022-03-06T19:18:36Z",
            "error": None,
            "result": {"success": True},
        },
        "reason": None,
        "seller_cpf": "369.779.868-59",
        "success": True,
        "uuid": "31a3e1a8-a318-4ca1-9a2d-8193252c1243",
        "vehicle": {
            "asset_value": 3499900,
            "chassi_code": None,
            "color": None,
            "fuel_type": {
                "credere_identifier": "5",
                "id": 123,
                "label": "Flex",
                "type": "fuel-type",
            },
            "id": 123,
            "km_mileage": None,
            "license_plate_code": None,
            "licensing_uf": "SP",
            "manufacture_year": 2015,
            "model_year": 2016,
            "renavam_code": None,
            "vehicle_model": {
                "available": True,
                "brand": "FIAT",
                "category": {
                    "credere_identifier": "veiculo",
                    "id": 123,
                    "label": "Veículo",
                    "type": "vehicle-category",
                },
                "fipe_code": "001343-9",
                "fuel_type": {
                    "credere_identifier": "5",
                    "id": 123,
                    "label": "Flex",
                    "type": "fuel-type",
                },
                "id": 123,
                "model_name": "UNO",
                "molicar_code": "01506928-0",
                "version": "VIVACE 1.0 8V EVO - Completo",
                "year_end": 2016,
                "year_start": 2010,
            },
            "zero_km": False,
        },
    }
}

SAMPLE_SIMULATION_LIST_RESPONSE = {"data": [SAMPLE_SIMULATION_RESPONSE["data"]]}


class TestSimulationsCreate:
    @respx.mock
    def test_create_simulation(self, sync_client: CredereClient) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        simulation_data = SimulationData.model_validate(
            SAMPLE_SIMULATION_CREATE_DATA["simulation"]
        )
        sim = sync_client.simulations.create(simulation_data)

        assert route.called
        assert isinstance(sim, SimulationResponse)
        assert sim.raw_response["assets_value"] == 3499900
        assert sim.raw_response["conditions"] is not None
        assert len(sim.raw_response["conditions"]) >= 1
        assert sim.raw_response["conditions"][0]["bank"] is not None
        assert sim.raw_response["conditions"][0]["bank"]["febraban_code"] == "033"


class TestSimulationsList:
    @respx.mock
    def test_list_simulations(self, sync_client: CredereClient) -> None:
        route = respx.get(LIST_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_LIST_RESPONSE)
        )

        sims = sync_client.simulations.list()

        assert route.called
        assert isinstance(sims, list)
        assert len(sims) == 1
        assert isinstance(sims[0], SimulationResponse)
        assert sims[0].raw_response["assets_value"] == 3499900
        assert sims[0].raw_response["conditions"] is not None
        assert len(sims[0].raw_response["conditions"]) >= 1
        assert sims[0].raw_response["conditions"][0]["bank"] is not None
        assert sims[0].raw_response["conditions"][0]["bank"]["febraban_code"] == "033"


class TestSimulationsGet:
    @respx.mock
    def test_get_simulation(self, sync_client: CredereClient) -> None:
        uuid = "abc-123-def"
        url = f"{SIMULATIONS_URL}/{uuid}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = sync_client.simulations.get(uuid)

        assert route.called
        assert isinstance(sim, SimulationResponse)


class TestSimulationsErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(LIST_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.simulations.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self, sync_client: CredereClient) -> None:
        url = f"{SIMULATIONS_URL}/nonexistent"
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
            sync_client.simulations.get("nonexistent")

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncSimulationsCreate:
    @respx.mock
    async def test_create_simulation(self, async_client: AsyncCredereClient) -> None:
        route = respx.post(SIMULATIONS_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        simulation_data = SimulationData.model_validate(
            SAMPLE_SIMULATION_CREATE_DATA["simulation"]
        )
        sim = await async_client.simulations.create(simulation_data)

        assert route.called
        assert isinstance(sim, SimulationResponse)
        assert sim.raw_response["assets_value"] == 3499900
        assert sim.raw_response["conditions"] is not None
        assert len(sim.raw_response["conditions"]) >= 1
        assert sim.raw_response["conditions"][0]["bank"] is not None
        assert sim.raw_response["conditions"][0]["bank"]["febraban_code"] == "033"


class TestAsyncSimulationsList:
    @respx.mock
    async def test_list_simulations(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(LIST_URL).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_LIST_RESPONSE)
        )

        sims = await async_client.simulations.list()

        assert route.called
        assert isinstance(sims, list)
        assert len(sims) == 1
        assert isinstance(sims[0], SimulationResponse)
        assert sims[0].raw_response["assets_value"] == 3499900
        assert sims[0].raw_response["conditions"] is not None
        assert len(sims[0].raw_response["conditions"]) >= 1
        assert sims[0].raw_response["conditions"][0]["bank"] is not None
        assert sims[0].raw_response["conditions"][0]["bank"]["febraban_code"] == "033"


class TestAsyncSimulationsGet:
    @respx.mock
    async def test_get_simulation(self, async_client: AsyncCredereClient) -> None:
        uuid = "abc-123-def"
        url = f"{SIMULATIONS_URL}/{uuid}"
        route = respx.get(url).mock(
            return_value=httpx.Response(200, json=SAMPLE_SIMULATION_RESPONSE)
        )

        sim = await async_client.simulations.get(uuid)

        assert route.called
        assert isinstance(sim, SimulationResponse)


class TestAsyncSimulationsErrorMapping:
    @respx.mock
    async def test_401_raises_authentication_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        respx.get(LIST_URL).mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await async_client.simulations.list()

        assert exc_info.value.status_code == 401

    @respx.mock
    async def test_404_raises_not_found_error(
        self, async_client: AsyncCredereClient
    ) -> None:
        url = f"{SIMULATIONS_URL}/nonexistent"
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
            await async_client.simulations.get("nonexistent")

        assert exc_info.value.status_code == 404
