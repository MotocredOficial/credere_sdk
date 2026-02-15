"""Sync and async resource classes for the Plus Returns endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.plus_returns import PlusReturnRule, PlusReturnRuleCreateRequest

_BASE_PATH = "/v1/plus_return_rules"


class PlusReturns:
    """Synchronous plus returns resource."""

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
        data: PlusReturnRuleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"plus_return_rule": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    def list(self, *, store_id: int | None = None) -> list[PlusReturnRule]:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [PlusReturnRule.model_validate(item) for item in response.json()]

    def get(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    def update(
        self,
        id: int,
        data: PlusReturnRuleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = self._client.patch(
                f"{_BASE_PATH}/{id}",
                json={"plus_return_rule": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    def delete(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> None:
        try:
            response = self._client.delete(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)

    def activate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/activate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    def deactivate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/deactivate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])


class AsyncPlusReturns:
    """Asynchronous plus returns resource."""

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
        data: PlusReturnRuleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"plus_return_rule": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    async def list(self, *, store_id: int | None = None) -> list[PlusReturnRule]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [PlusReturnRule.model_validate(item) for item in response.json()]

    async def get(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    async def update(
        self,
        id: int,
        data: PlusReturnRuleCreateRequest,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = await self._client.patch(
                f"{_BASE_PATH}/{id}",
                json={"plus_return_rule": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    async def delete(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> None:
        try:
            response = await self._client.delete(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)

    async def activate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/activate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])

    async def deactivate(
        self,
        id: int,
        *,
        store_id: int | None = None,
    ) -> PlusReturnRule:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/deactivate",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return PlusReturnRule.model_validate(response.json()["plus_return_rule"])
