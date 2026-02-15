"""Sync and async HTTP clients for the Credere API."""

from __future__ import annotations

import httpx

from credere.auth import APIKeyAuth
from credere.resources.leads import AsyncLeads, Leads
from credere.resources.proposal_attempts import AsyncProposalAttempts, ProposalAttempts
from credere.resources.proposals import AsyncProposals, Proposals
from credere.resources.simulations import AsyncSimulations, Simulations
from credere.resources.stores import AsyncStores, Stores
from credere.resources.users import AsyncUsers, Users
from credere.resources.vehicle_models import AsyncVehicleModels, VehicleModels

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
        self.proposals = Proposals(self._http, store_id=store_id)
        self.simulations = Simulations(self._http, store_id=store_id)
        self.vehicle_models = VehicleModels(self._http, store_id=store_id)
        self.proposal_attempts = ProposalAttempts(self._http, store_id=store_id)
        self.stores = Stores(self._http, store_id=store_id)
        self.users = Users(self._http, store_id=store_id)

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
        self.proposals = AsyncProposals(self._http, store_id=store_id)
        self.simulations = AsyncSimulations(self._http, store_id=store_id)
        self.vehicle_models = AsyncVehicleModels(self._http, store_id=store_id)
        self.proposal_attempts = AsyncProposalAttempts(self._http, store_id=store_id)
        self.stores = AsyncStores(self._http, store_id=store_id)
        self.users = AsyncUsers(self._http, store_id=store_id)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncCredereClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
