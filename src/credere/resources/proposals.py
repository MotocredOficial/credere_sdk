"""Sync and async resource classes for the Proposals endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.proposals import (
    ProposalData,
    ProposalResponse,
)

_BASE_PATH = "api/v1/proposals"


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
        data: ProposalData,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
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
        return ProposalResponse.model_validate(response.json()["complete_proposal"])

    def list(self, *, store_id: int | None = None) -> list[ProposalResponse]:
        try:
            response = self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            ProposalResponse.model_validate(item)
            for item in response.json()["proposals"]
        ]

    def get(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalResponse.model_validate(response.json()["proposal"])

    def update(
        self,
        id: str,
        data: ProposalData,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
        try:
            response = self._client.put(
                f"{_BASE_PATH}/{id}",
                json={
                    "proposal": data.model_dump(exclude_none=True).update({"id": id})
                },
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalResponse.model_validate(response.json())

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
        data: ProposalData,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
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
        return ProposalResponse.model_validate(response.json()["complete_proposal"])

    async def list(self, *, store_id: int | None = None) -> list[ProposalResponse]:
        try:
            response = await self._client.get(
                _BASE_PATH,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            ProposalResponse.model_validate(item)
            for item in response.json()["proposals"]
        ]

    async def get(
        self,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalResponse.model_validate(response.json()["proposal"])

    async def update(
        self,
        id: str,
        data: ProposalData,
        *,
        store_id: int | None = None,
    ) -> ProposalResponse:
        try:
            response = await self._client.put(
                f"{_BASE_PATH}/{id}",
                json={
                    "proposal": data.model_dump(exclude_none=True).update({"id": id})
                },
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalResponse.model_validate(response.json())

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
