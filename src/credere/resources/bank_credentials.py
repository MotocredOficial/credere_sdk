"""Sync and async resource classes for the Bank Credentials endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.bank_credentials import IntegratedBank


class BankCredentials:
    """Synchronous bank credentials resource."""

    def __init__(self, client: httpx.Client, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    def persist(
        self,
        store_id: int,
    ) -> dict[str, Any]:
        try:
            response = self._client.get(
                f"/v1/stores/{store_id}/persist_cnpj_bank_credentials",
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()

    def list(
        self,
        *,
        store_id: int,
        bank_codes: list[str] | None = None,
    ) -> list[IntegratedBank]:
        params = {}
        if bank_codes:
            params["bank_codes"] = bank_codes
        try:
            response = self._client.get(
                f"/v1/stores/{store_id}/integrated_banks",
                headers=self._headers(),
                params=params or None,
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            IntegratedBank.model_validate(item)
            for item in response.json()["integrated_banks"]
        ]


class AsyncBankCredentials:
    """Asynchronous bank credentials resource."""

    def __init__(self, client: httpx.AsyncClient, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    async def persist(
        self,
        store_id: int,
    ) -> dict[str, Any]:
        try:
            response = await self._client.get(
                f"/v1/stores/{store_id}/persist_cnpj_bank_credentials",
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()

    async def list(
        self,
        *,
        store_id: int,
        bank_codes: list[str] | None = None,
    ) -> list[IntegratedBank]:
        params = {}
        if bank_codes:
            params["bank_codes"] = bank_codes
        try:
            response = await self._client.get(
                f"/v1/stores/{store_id}/integrated_banks",
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            IntegratedBank.model_validate(item)
            for item in response.json()["integrated_banks"]
        ]
