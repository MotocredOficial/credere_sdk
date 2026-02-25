"""Sync and async resource classes for the Proposal Attempts endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.proposal_attempts import (
    ProposalAttemptCreateRequest,
)
from credere.models.proposals import ProposalAttemptResponse


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
    ) -> ProposalAttemptResponse:
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
        return ProposalAttemptResponse.model_validate(
            response.json()["proposal_attempt"]
        )

    def list(
        self,
        proposal_id: str,
        *,
        store_id: int | None = None,
    ) -> list[ProposalAttemptResponse]:
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
            ProposalAttemptResponse.model_validate(item)
            for item in response.json()["proposal_attempts"]
        ]

    def get(
        self,
        proposal_id: str,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttemptResponse:
        try:
            response = self._client.get(
                f"{_base_path(proposal_id)}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttemptResponse.model_validate(
            response.json()["proposal_attempt"]
        )

    def update(
        self,
        proposal_id: str,
        id: str,
        data: ProposalAttemptResponse,
        *,
        store_id: int | None = None,
    ) -> ProposalAttemptResponse:
        try:
            response = self._client.put(
                f"{_base_path(proposal_id)}/{id}",
                json=data.model_dump(exclude_none=True, mode="json"),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttemptResponse.model_validate(response.json())


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
    ) -> ProposalAttemptResponse:
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
        return ProposalAttemptResponse.model_validate(
            response.json()["proposal_attempt"]
        )

    async def list(
        self,
        proposal_id: str,
        *,
        store_id: int | None = None,
    ) -> list[ProposalAttemptResponse]:
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
            ProposalAttemptResponse.model_validate(item)
            for item in response.json()["proposal_attempts"]
        ]

    async def get(
        self,
        proposal_id: str,
        id: str,
        *,
        store_id: int | None = None,
    ) -> ProposalAttemptResponse:
        try:
            response = await self._client.get(
                f"{_base_path(proposal_id)}/{id}",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttemptResponse.model_validate(
            response.json()["proposal_attempt"]
        )

    async def update(
        self,
        proposal_id: str,
        id: str,
        data: ProposalAttemptResponse,
        *,
        store_id: int | None = None,
    ) -> ProposalAttemptResponse:
        try:
            response = await self._client.put(
                f"{_base_path(proposal_id)}/{id}",
                json=data.model_dump(exclude_none=True, mode="json"),
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return ProposalAttemptResponse.model_validate(response.json())

