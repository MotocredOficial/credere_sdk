"""Tests for the Utilities resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError
from credere.models.simulations import Bank
from credere.models.utilities import Domain

BASE_URL = "https://api.credere.com"

SAMPLE_DOMAIN = {
    "id": 1,
    "type": "gender",
    "credere_identifier": "male",
    "label": "Masculino",
}

SAMPLE_BANK = {
    "id": 1,
    "febraban_code": "001",
    "name": "Banco do Brasil",
    "nickname": "BB",
}

SAMPLE_VEHICLE = {"name": "Civic", "brand": "Honda"}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestUtilitiesDomains:
    @respx.mock
    def test_domains_returns_list_of_domain(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/domains").mock(
            return_value=httpx.Response(200, json=[SAMPLE_DOMAIN])
        )

        result = sync_client.utilities.domains()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert result[0].type == "gender"
        assert result[0].credere_identifier == "male"
        assert result[0].label == "Masculino"


class TestUtilitiesLeadDomains:
    @respx.mock
    def test_lead_domains_returns_list_of_domain(
        self, sync_client: CredereClient
    ) -> None:
        route = respx.get(f"{BASE_URL}/v1/banks_api/domains").mock(
            return_value=httpx.Response(200, json=[SAMPLE_DOMAIN])
        )

        result = sync_client.utilities.lead_domains()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert result[0].type == "gender"
        assert result[0].credere_identifier == "male"
        assert result[0].label == "Masculino"


class TestUtilitiesBanks:
    @respx.mock
    def test_banks_returns_list_of_bank(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/banks").mock(
            return_value=httpx.Response(200, json={"banks": [SAMPLE_BANK]})
        )

        result = sync_client.utilities.banks()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Bank)
        assert result[0].id == 1
        assert result[0].febraban_code == "001"
        assert result[0].name == "Banco do Brasil"
        assert result[0].nickname == "BB"


class TestUtilitiesVehicleByPlate:
    @respx.mock
    def test_vehicle_by_plate_returns_dict(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/vehicles/license_plate/ABC1234").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE)
        )

        result = sync_client.utilities.vehicle_by_plate("ABC1234")

        assert route.called
        assert isinstance(result, dict)
        assert result["name"] == "Civic"
        assert result["brand"] == "Honda"


class TestUtilitiesVehicleByChassis:
    @respx.mock
    def test_vehicle_by_chassis_returns_dict(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/vehicles/chassi_code/9BWZZZ377VT004251").mock(
            return_value=httpx.Response(200, json=SAMPLE_VEHICLE)
        )

        result = sync_client.utilities.vehicle_by_chassis("9BWZZZ377VT004251")

        assert route.called
        assert isinstance(result, dict)
        assert result["name"] == "Civic"
        assert result["brand"] == "Honda"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(f"{BASE_URL}/v1/domains").mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.utilities.domains()

        assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncUtilitiesDomains:
    @respx.mock
    async def test_async_domains_returns_list_of_domain(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{BASE_URL}/v1/domains").mock(
            return_value=httpx.Response(200, json=[SAMPLE_DOMAIN])
        )

        result = await async_client.utilities.domains()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Domain)
        assert result[0].id == 1
        assert result[0].type == "gender"
        assert result[0].credere_identifier == "male"
        assert result[0].label == "Masculino"


class TestAsyncUtilitiesBanks:
    @respx.mock
    async def test_async_banks_returns_list_of_bank(
        self, async_client: AsyncCredereClient
    ) -> None:
        route = respx.get(f"{BASE_URL}/v1/banks").mock(
            return_value=httpx.Response(200, json={"banks": [SAMPLE_BANK]})
        )

        result = await async_client.utilities.banks()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Bank)
        assert result[0].id == 1
        assert result[0].febraban_code == "001"
        assert result[0].name == "Banco do Brasil"
        assert result[0].nickname == "BB"
