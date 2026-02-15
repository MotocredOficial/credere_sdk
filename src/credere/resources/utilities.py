"""Sync and async resource classes for the Utilities endpoints."""

from __future__ import annotations

from typing import Any

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.simulations import Bank
from credere.models.utilities import Domain


class Utilities:
    """Synchronous utilities resource."""

    def __init__(self, client: httpx.Client, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    def domains(self, *, store_id: int | None = None) -> list[Domain]:
        try:
            response = self._client.get(
                "/v1/domains",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Domain.model_validate(item) for item in response.json()]

    def lead_domains(self, *, store_id: int | None = None) -> list[Domain]:
        try:
            response = self._client.get(
                "/v1/banks_api/domains",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Domain.model_validate(item) for item in response.json()]

    def banks(self, *, store_id: int | None = None) -> list[Bank]:
        try:
            response = self._client.get(
                "/v1/banks",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Bank.model_validate(item) for item in response.json()["banks"]]

    def vehicle_by_plate(
        self,
        plate: str,
        *,
        store_id: int | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._client.get(
                f"/v1/vehicles/license_plate/{plate}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()

    def vehicle_by_chassis(
        self,
        chassi: str,
        *,
        store_id: int | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._client.get(
                f"/v1/vehicles/chassi_code/{chassi}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()


class AsyncUtilities:
    """Asynchronous utilities resource."""

    def __init__(self, client: httpx.AsyncClient, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    async def domains(self, *, store_id: int | None = None) -> list[Domain]:
        try:
            response = await self._client.get(
                "/v1/domains",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Domain.model_validate(item) for item in response.json()]

    async def lead_domains(self, *, store_id: int | None = None) -> list[Domain]:
        try:
            response = await self._client.get(
                "/v1/banks_api/domains",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Domain.model_validate(item) for item in response.json()]

    async def banks(self, *, store_id: int | None = None) -> list[Bank]:
        try:
            response = await self._client.get(
                "/v1/banks",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Bank.model_validate(item) for item in response.json()["banks"]]

    async def vehicle_by_plate(
        self,
        plate: str,
        *,
        store_id: int | None = None,
    ) -> dict[str, Any]:
        try:
            response = await self._client.get(
                f"/v1/vehicles/license_plate/{plate}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()

    async def vehicle_by_chassis(
        self,
        chassi: str,
        *,
        store_id: int | None = None,
    ) -> dict[str, Any]:
        try:
            response = await self._client.get(
                f"/v1/vehicles/chassi_code/{chassi}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()
