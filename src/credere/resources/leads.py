"""Sync and async resource classes for the Leads endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.leads import Lead, LeadCreateRequest, LeadRequiredFields

_BASE_PATH = "/v1/banks_api/leads"


class Leads:
    """Synchronous leads resource."""

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
        data: LeadCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"lead": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise  # unreachable, satisfies type checker
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    def update(
        self,
        cpf_cnpj: str,
        data: LeadCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = self._client.patch(
                f"{_BASE_PATH}/{cpf_cnpj}",
                json={"lead": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    def delete(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> None:
        try:
            response = self._client.delete(
                f"{_BASE_PATH}/{cpf_cnpj}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)

    def list(self, *, store_id: int | None = None) -> list[Lead]:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Lead.model_validate(item) for item in response.json()["data"]]

    def get(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{cpf_cnpj}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    def required_fields(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> LeadRequiredFields:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{cpf_cnpj}/required_fields",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return LeadRequiredFields.model_validate(response.json()["data"])


class AsyncLeads:
    """Asynchronous leads resource."""

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
        data: LeadCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"lead": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    async def update(
        self,
        cpf_cnpj: str,
        data: LeadCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = await self._client.patch(
                f"{_BASE_PATH}/{cpf_cnpj}",
                json={"lead": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    async def delete(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> None:
        try:
            response = await self._client.delete(
                f"{_BASE_PATH}/{cpf_cnpj}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)

    async def list(self, *, store_id: int | None = None) -> list[Lead]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Lead.model_validate(item) for item in response.json()["data"]]

    async def get(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> Lead:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{cpf_cnpj}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Lead.model_validate(response.json()["data"])

    async def required_fields(
        self,
        cpf_cnpj: str,
        *,
        store_id: int | None = None,
    ) -> LeadRequiredFields:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{cpf_cnpj}/required_fields",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return LeadRequiredFields.model_validate(response.json()["data"])
