"""Sync and async resource classes for the Vehicle Models endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from credere._response import handle_request_error, raise_for_status
from credere.models.vehicle_models import VehicleModel, VehiclePrice

_MODELS_PATH = "api/v1/vehicle_models"
_PRICES_PATH = "api/v1/vehicle_prices"


class VehicleModels:
    """Synchronous vehicle models resource."""

    def __init__(self, client: httpx.Client, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    def list(
        self,
        *,
        store_id: int | None = None,
        per_page: int | None = None,
        molicar_code: str | None = None,
        fipe_code: str | None = None,
        **params: Any,
    ) -> list[VehicleModel]:
        query_params = {
            **params,
            "per_page": per_page,
            "molicar_code": molicar_code,
            "fipe_code": fipe_code,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}

        try:
            response = self._client.get(
                _MODELS_PATH,
                params=query_params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            VehicleModel.model_validate(item)
            for item in response.json()["vehicle_models"]
        ]

    def search(
        self,
        q: str,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> VehicleModel:
        query_params = {
            **params,
            "q": q,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}
        try:
            response = self._client.get(
                f"{_MODELS_PATH}/search",
                params=query_params,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return VehicleModel.model_validate(response.json()["vehicle_model"])

    def prices(
        self,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> list[VehiclePrice]:
        try:
            response = self._client.get(
                _PRICES_PATH,
                params=params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            VehiclePrice.model_validate(item)
            for item in response.json()["vehicle_prices"]
        ]


class AsyncVehicleModels:
    """Asynchronous vehicle models resource."""

    def __init__(self, client: httpx.AsyncClient, store_id: int | None = None) -> None:
        self._client = client
        self._store_id = store_id

    def _headers(self, store_id: int | None = None) -> dict[str, str]:
        sid = store_id if store_id is not None else self._store_id
        if sid is not None:
            return {"Store-Id": str(sid)}
        return {}

    async def list(
        self,
        *,
        store_id: int | None = None,
        per_page: int | None = None,
        molicar_code: str | None = None,
        fipe_code: str | None = None,
        **params: Any,
    ) -> list[VehicleModel]:
        query_params = {
            **params,
            "per_page": per_page,
            "molicar_code": molicar_code,
            "fipe_code": fipe_code,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}

        try:
            response = await self._client.get(
                _MODELS_PATH,
                params=query_params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            VehicleModel.model_validate(item)
            for item in response.json()["vehicle_models"]
        ]

    async def search(
        self,
        q: str,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> VehicleModel:
        query_params = {
            **params,
            "q": q,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}
        try:
            response = await self._client.get(
                f"{_MODELS_PATH}/search",
                params=query_params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return VehicleModel.model_validate(response.json()["vehicle_model"])

    async def prices(
        self,
        *,
        store_id: int | None = None,
        **params: Any,
    ) -> list[VehiclePrice]:
        try:
            response = await self._client.get(
                _PRICES_PATH,
                params=params or None,
                headers=self._headers(store_id),
            )
        except httpx.HTTPError as exc:
            handle_request_error(exc)
            raise
        raise_for_status(response)
        return [
            VehiclePrice.model_validate(item)
            for item in response.json()["vehicle_prices"]
        ]
