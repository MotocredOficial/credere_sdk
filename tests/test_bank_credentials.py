"""Tests for the BankCredentials resource (sync + async)."""

import httpx
import pytest
import respx

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import AuthenticationError
from credere.models.bank_credentials import IntegratedBank

BASE_URL = "https://api.credere.com"
STORE_ID = 99

SAMPLE_INTEGRATED_BANK = {
    "id": 1,
    "store_id": 99,
    "credentials_status": "active",
    "created_at": "2024-01-15T10:00:00-03:00",
    "updated_at": "2024-01-15T10:00:00-03:00",
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestBankCredentialsPersist:
    @respx.mock
    def test_persist(self, sync_client: CredereClient) -> None:
        route = respx.get(
            f"{BASE_URL}/v1/stores/{STORE_ID}/persist_cnpj_bank_credentials"
        ).mock(return_value=httpx.Response(200, json={"status": "ok"}))

        result = sync_client.bank_credentials.persist(STORE_ID)

        assert route.called
        assert result == {"status": "ok"}


class TestBankCredentialsList:
    @respx.mock
    def test_list(self, sync_client: CredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/integrated_banks").mock(
            return_value=httpx.Response(
                200,
                json={"integrated_banks": [SAMPLE_INTEGRATED_BANK]},
            )
        )

        result = sync_client.bank_credentials.list(STORE_ID)

        assert route.called
        assert len(result) == 1
        assert isinstance(result[0], IntegratedBank)
        assert result[0].credentials_status == "active"


# ---------------------------------------------------------------------------
# Error mapping tests
# ---------------------------------------------------------------------------


class TestErrorMapping:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: CredereClient) -> None:
        respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/integrated_banks").mock(
            return_value=httpx.Response(
                401,
                json={"error": {"message": "Unauthorized", "status": 401}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            sync_client.bank_credentials.list(STORE_ID)

        assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncBankCredentialsList:
    @respx.mock
    async def test_async_list(self, async_client: AsyncCredereClient) -> None:
        route = respx.get(f"{BASE_URL}/v1/stores/{STORE_ID}/integrated_banks").mock(
            return_value=httpx.Response(
                200,
                json={"integrated_banks": [SAMPLE_INTEGRATED_BANK]},
            )
        )

        result = await async_client.bank_credentials.list(STORE_ID)

        assert route.called
        assert len(result) == 1
        assert isinstance(result[0], IntegratedBank)
        assert result[0].credentials_status == "active"
