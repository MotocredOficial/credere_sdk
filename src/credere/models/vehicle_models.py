"""Pydantic models for the Vehicle Models resource."""

from __future__ import annotations

from pydantic import BaseModel


class VehicleBrand(BaseModel):
    id: int | None = None
    name: str | None = None


class Fuel(BaseModel):
    object_type: str | None = None
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str | None = None


class VehicleType(BaseModel):
    id: int | None = None
    name: str | None = None


class VehicleModelSummary(BaseModel):
    id: int | None = None
    name: str | None = None
    brand: str | None = None
    molicar_code: str | None = None
    version: str | None = None
    year_end: int | None = None
    year_start: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    fuel: Fuel | None = None


class Store(BaseModel):
    id: int | None = None
    name: str | None = None
    display_name: str | None = None
    uf: str | None = None
    limit_vehicle_prices: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class VehicleModel(BaseModel):
    object_type: str | None = None
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str | None = None
    brand: str | None = None
    molicar_code: str | None = None
    version: str | None = None
    year_end: int | None = None
    year_start: int | None = None
    active: bool | None = None
    public_price_cents: int | None = None
    public_price_as_string: str | None = None
    publish: bool | None = None
    fipe_code: str | None = None
    public_picture: str | None = None
    vehicle_brand: VehicleBrand | None = None
    fuel: Fuel | None = None
    vehicle_type: VehicleType | None = None


class VehiclePrice(BaseModel):
    id: int | None = None
    store_id: int | None = None
    min_price_cents: int | None = None
    default_price_cents: int | None = None
    active: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    vehicle_model: VehicleModelSummary | None = None
    store: Store | None = None
