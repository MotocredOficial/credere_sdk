"""Sync and async resource classes for the Customers endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.customers import Customer, CustomerCreateRequest

_BASE_PATH = "/v1/customers"


class Customers:
    """Synchronous customers resource."""

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
        data: CustomerCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"customer": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    def update(
        self,
        id: int,
        data: CustomerCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = self._client.patch(
                f"{_BASE_PATH}/{id}",
                json={"customer": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    def list(self, *, store_id: int | None = None) -> list[Customer]:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Customer.model_validate(item) for item in response.json()["customers"]]

    def get(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    def find(
        self,
        *,
        store_id: int | None = None,
        **params: str,
    ) -> Customer:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/find",
                params=params,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])


class AsyncCustomers:
    """Asynchronous customers resource."""

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
        data: CustomerCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"customer": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    async def update(
        self,
        id: int,
        data: CustomerCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = await self._client.patch(
                f"{_BASE_PATH}/{id}",
                json={"customer": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    async def list(self, *, store_id: int | None = None) -> list[Customer]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Customer.model_validate(item) for item in response.json()["customers"]]

    async def get(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Customer:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])

    async def find(
        self,
        *,
        store_id: int | None = None,
        **params: str,
    ) -> Customer:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/find",
                params=params,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Customer.model_validate(response.json()["customer"])
