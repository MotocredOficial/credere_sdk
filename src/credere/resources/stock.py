"""Sync and async resource classes for the Stock / Inventory endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.stock import StockVehicle, StockVehicleCreateRequest

_BASE_PATH = "/v1/vehicles"


class Stock:
    """Synchronous stock resource."""

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
        data: StockVehicleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"vehicle": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])

    def list(self, *, store_id: int | None = None) -> list[StockVehicle]:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [StockVehicle.model_validate(item) for item in response.json()]

    def update(
        self,
        id: int,
        data: StockVehicleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = self._client.put(
                f"{_BASE_PATH}/{id}",
                json={"vehicle": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])

    def remove(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = self._client.put(
                f"{_BASE_PATH}/{id}/remove_from_stock",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])


class AsyncStock:
    """Asynchronous stock resource."""

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
        data: StockVehicleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"vehicle": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])

    async def list(self, *, store_id: int | None = None) -> list[StockVehicle]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [StockVehicle.model_validate(item) for item in response.json()]

    async def update(
        self,
        id: int,
        data: StockVehicleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = await self._client.put(
                f"{_BASE_PATH}/{id}",
                json={"vehicle": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])

    async def remove(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> StockVehicle:
        try:
            response = await self._client.put(
                f"{_BASE_PATH}/{id}/remove_from_stock",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return StockVehicle.model_validate(response.json()["vehicle"])
