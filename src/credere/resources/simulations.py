"""Sync and async resource classes for the Simulations endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.simulations import SimulationData, SimulationResponse

_BASE_PATH = "/v1/banks_api/simulations"
_LIST_PATH = "/v1/proposal_simulations"


class Simulations:
    """Synchronous simulations resource."""

    def __init__(self, client: httpx.Client, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    def create(
        self,
        data: SimulationData,
        *,
        store_id: int | None = None,
    ) -> SimulationResponse:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"simulation": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise  # unreachable, satisfies type checker
        raise_for_status(response)
        payload = response.json()["data"]
        return SimulationResponse(
            simulation_id=payload["uuid"],
            raw_response=payload,
        )

    def list(self, *, store_id: int | None = None) -> list[SimulationResponse]:
        try:
            response = self._client.get(
                _LIST_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            SimulationResponse(
                simulation_id=item["uuid"],
                raw_response=item,
            )
            for item in response.json()["data"]
        ]

    def get(
        self,
        uuid: str,
        *,
        store_id: int | None = None,
    ) -> SimulationResponse:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{uuid}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        payload = response.json()["data"]
        return SimulationResponse(
            simulation_id=payload["uuid"],
            raw_response=payload,
        )


class AsyncSimulations:
    """Asynchronous simulations resource."""

    def __init__(self, client: httpx.AsyncClient, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    async def create(
        self,
        data: SimulationData,
        *,
        store_id: int | None = None,
    ) -> SimulationResponse:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"simulation": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        payload = response.json()["data"]
        return SimulationResponse(
            simulation_id=payload["uuid"],
            raw_response=payload,
        )

    async def list(self, *, store_id: int | None = None) -> list[SimulationResponse]:
        try:
            response = await self._client.get(
                _LIST_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            SimulationResponse(
                simulation_id=item["uuid"],
                raw_response=item,
            )
            for item in response.json()["data"]
        ]

    async def get(
        self,
        uuid: str,
        *,
        store_id: int | None = None,
    ) -> SimulationResponse:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{uuid}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        payload = response.json()["data"]
        return SimulationResponse(
            simulation_id=payload["uuid"],
            raw_response=payload,
        )
