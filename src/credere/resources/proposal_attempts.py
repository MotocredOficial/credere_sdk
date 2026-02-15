"""Sync and async resource classes for the Proposal Attempts endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.proposal_attempts import (
    ProposalAttempt,
    ProposalAttemptCreateRequest,
)


def _base_path(proposal_id: str) -> str:
    return f"/v1/proposals/{proposal_id}/proposal_attempts"


class ProposalAttempts:
    """Synchronous proposal attempts resource."""

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
        proposal_id: str,
        data: ProposalAttemptCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = self._client.post(
                _base_path(proposal_id),
                json=data.model_dump(exclude_none=True),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    def list(
        self,
        proposal_id: str,
        *,
        store_id: int | None = None,
    ) -> list[ProposalAttempt]:
        try:
            response = self._client.get(
                _base_path(proposal_id),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            ProposalAttempt.model_validate(item) for item in response.json()["data"]
        ]

    def get(
        self,
        proposal_id: str,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = self._client.get(
                f"{_base_path(proposal_id)}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    def update(
        self,
        proposal_id: str,
        id: str,
        data: ProposalAttemptCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = self._client.put(
                f"{_base_path(proposal_id)}/{id}",
                json=data.model_dump(exclude_none=True),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    def perform_action(
        self,
        proposal_id: str,
        id: str,
        action: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = self._client.get(
                f"{_base_path(proposal_id)}/{id}/{action}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])


class AsyncProposalAttempts:
    """Asynchronous proposal attempts resource."""

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
        proposal_id: str,
        data: ProposalAttemptCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = await self._client.post(
                _base_path(proposal_id),
                json=data.model_dump(exclude_none=True),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    async def list(
        self,
        proposal_id: str,
        *,
        store_id: int | None = None,
    ) -> list[ProposalAttempt]:
        try:
            response = await self._client.get(
                _base_path(proposal_id),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            ProposalAttempt.model_validate(item) for item in response.json()["data"]
        ]

    async def get(
        self,
        proposal_id: str,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = await self._client.get(
                f"{_base_path(proposal_id)}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    async def update(
        self,
        proposal_id: str,
        id: str,
        data: ProposalAttemptCreateRequest,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = await self._client.put(
                f"{_base_path(proposal_id)}/{id}",
                json=data.model_dump(exclude_none=True),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])

    async def perform_action(
        self,
        proposal_id: str,
        id: str,
        action: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttempt:
        try:
            response = await self._client.get(
                f"{_base_path(proposal_id)}/{id}/{action}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttempt.model_validate(response.json()["data"])
