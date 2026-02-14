"""Tests for client instantiation and auth header injection."""

import httpx
import respx

from credere.client import AsyncCredereClient, CredereClient

API_KEY = "sk-test-key"
BASE_URL = "https://api.credere.com"


class TestCredereClient:
    def test_injects_auth_header(self, sync_client: CredereClient) -> None:
        with respx.mock:
            route = respx.get(f"{BASE_URL}/health").mock(
                return_value=httpx.Response(200, json={"ok": True})
            )

            response = sync_client._http.get("/health")

            assert route.called
            auth = route.calls.last.request.headers["Authorization"]
            assert auth == f"Bearer {API_KEY}"
            assert response.status_code == 200

    def test_context_manager(self) -> None:
        with CredereClient(api_key=API_KEY) as client:
            assert client._http.is_closed is False
        assert client._http.is_closed is True


class TestAsyncCredereClient:
    async def test_injects_auth_header(self, async_client: AsyncCredereClient) -> None:
        with respx.mock:
            route = respx.get(f"{BASE_URL}/health").mock(
                return_value=httpx.Response(200, json={"ok": True})
            )

            response = await async_client._http.get("/health")

            assert route.called
            auth = route.calls.last.request.headers["Authorization"]
            assert auth == f"Bearer {API_KEY}"
            assert response.status_code == 200

    async def test_context_manager(self) -> None:
        async with AsyncCredereClient(api_key=API_KEY) as client:
            assert client._http.is_closed is False
        assert client._http.is_closed is True
