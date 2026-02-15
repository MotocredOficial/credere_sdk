"""Sync and async resource classes for the Users endpoint."""

from __future__ import annotations

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.users import User

_BASE_PATH = "/v1/users"


class Users:
    """Synchronous users resource."""

    def __init__(self, client: httpx.Client, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    def current(self) -> User:
        try:
            response = self._client.get(f"{_BASE_PATH}/current")
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return User.model_validate(response.json()["user"])

    def proposals_filter_list(
        self,
        *,
        store_id: int | None = None,
    ) -> list[User]:
        try:
            response = self._client.get(
                f"{_BASE_PATH}/proposals_filter_list",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [User.model_validate(item) for item in response.json()["users"]]


class AsyncUsers:
    """Asynchronous users resource."""

    def __init__(self, client: httpx.AsyncClient, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    async def current(self) -> User:
        try:
            response = await self._client.get(f"{_BASE_PATH}/current")
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return User.model_validate(response.json()["user"])

    async def proposals_filter_list(
        self,
        *,
        store_id: int | None = None,
    ) -> list[User]:
        try:
            response = await self._client.get(
                f"{_BASE_PATH}/proposals_filter_list",
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [User.model_validate(item) for item in response.json()["users"]]
