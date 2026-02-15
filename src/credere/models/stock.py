"""Pydantic models for the Stock / Inventory resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StockVehicleCreateRequest(BaseModel):
    """Input model for creating or updating a stock vehicle."""

    model_config = ConfigDict(extra="allow")

    vehicle_model_id: int | None = None
    store_id: int | None = None
    price_cents: int | None = None
    description: str | None = None


class StockVehicle(BaseModel):
    """Stock vehicle as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    price_cents: int | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
