"""Sync and async resource classes for the Proposals endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.proposals import (
    ProposalCreateRequest,
    ProposalCreateResponse,
    ProposalGetResponse,
    ProposalListResponse,
    ProposalUpdateRequest,
)

_BASE_PATH = "/v1/proposals"


class Proposals:
    """Synchronous proposals resource."""

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
        data: ProposalCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalCreateResponse:
        try:
            response = self._client.post(
                _BASE_PATH,
                json={"proposal": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise  # unreachable, satisfies type checker
        raise_for_status(response)
        return ProposalCreateResponse.model_validate(response.json())

    def list(self, *, store_id: int | None = None) -> ProposalListResponse:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalListResponse.model_validate(response.json())

    def get(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    def update(
        self,
        id: str,
        data: ProposalUpdateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalCreateResponse:
        try:
            response = self._client.put(
                f"{_BASE_PATH}/{id}",
                json={"proposal": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalCreateResponse.model_validate(response.json())

    def delete(
        self,
        id: str,
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

    def get_ownership(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/get_ownership",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    def leave_ownership(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/leave_ownership",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    def activity_log(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> list[dict]:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}/activity_log",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()


class AsyncProposals:
    """Asynchronous proposals resource."""

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
        data: ProposalCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalCreateResponse:
        try:
            response = await self._client.post(
                _BASE_PATH,
                json={"proposal": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalCreateResponse.model_validate(response.json())

    async def list(self, *, store_id: int | None = None) -> ProposalListResponse:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalListResponse.model_validate(response.json())

    async def get(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    async def update(
        self,
        id: str,
        data: ProposalUpdateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalCreateResponse:
        try:
            response = await self._client.put(
                f"{_BASE_PATH}/{id}",
                json={"proposal": data.model_dump(exclude_none=True)},
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalCreateResponse.model_validate(response.json())

    async def delete(
        self,
        id: str,
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

    async def get_ownership(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/get_ownership",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    async def leave_ownership(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalGetResponse:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/leave_ownership",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalGetResponse.model_validate(response.json())

    async def activity_log(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> list[dict]:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}/activity_log",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return response.json()
