"""Pydantic models for the Stores resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StoreCreateRequest(BaseModel):
    """Input model for creating a store."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    display_name: str | None = None
    cnpj: str | None = None
    _persist_cnpj_bank_credentials: bool | None = None


class Store(BaseModel):
    """Store as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    object_type: str | None = None
    name: str | None = None
    display_name: str | None = None
    uf: str | None = None
    city: str | None = None
    cnpj: str | None = None
    new_vehicle_sales: bool | None = None
    used_vehicle_sales: bool | None = None
    publish: bool | None = None
    public_api_identifier: str | None = None
    avatar: dict | None = None
    limit_fi_performance_visibility: bool | None = None
    limit_simulation_bank_visibility: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
