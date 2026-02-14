"""Sync and async HTTP clients for the Credere API."""

from __future__ import annotations

import httpx

from credere.auth import APIKeyAuth
from credere.resources.leads import AsyncLeads, Leads
from credere.resources.simulations import AsyncSimulations, Simulations

_DEFAULT_BASE_URL = "https://api.credere.com"
_DEFAULT_TIMEOUT = 30.0


class CredereClient:
    """Synchronous client for the Credere API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        store_id: int | None = None,
    ) -> None:
        self._store_id = store_id
        self._http = httpx.Client(
            base_url=base_url,
            auth=APIKeyAuth(api_key),
            timeout=timeout,
        )
        self.leads = Leads(self._http, store_id=store_id)
        self.simulations = Simulations(self._http, store_id=store_id)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> CredereClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncCredereClient:
    """Asynchronous client for the Credere API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        store_id: int | None = None,
    ) -> None:
        self._store_id = store_id
        self._http = httpx.AsyncClient(
            base_url=base_url,
            auth=APIKeyAuth(api_key),
            timeout=timeout,
        )
        self.leads = AsyncLeads(self._http, store_id=store_id)
        self.simulations = AsyncSimulations(self._http, store_id=store_id)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncCredereClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
