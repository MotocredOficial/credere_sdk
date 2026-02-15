"""Sync and async resource classes for the Stores endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.stores import Store, StoreCreateRequest

_BASE_PATH = "/v1/stores"


class Stores:
    """Synchronous stores resource."""

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
        data: StoreCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"store": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])

    def list(
        self,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> list[Store]:
        try:
            response = self._client.get(
                _BASE_PATH,
                params=params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Store.model_validate(item) for item in response.json()["stores"]]

    def activate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/activate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])

    def deactivate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/deactivate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])


class AsyncStores:
    """Asynchronous stores resource."""

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
        data: StoreCreateRequest,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"store": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])

    async def list(
        self,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> list[Store]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                params=params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [Store.model_validate(item) for item in response.json()["stores"]]

    async def activate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/activate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])

    async def deactivate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> Store:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/deactivate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return Store.model_validate(response.json()["store"])
