"""Pydantic models for the Vehicle Models resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class VehicleBrand(BaseModel):
    """Vehicle brand as returned in vehicle model responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None


class VehicleFuel(BaseModel):
    """Vehicle fuel type as returned in vehicle model responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    object_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class VehicleType(BaseModel):
    """Vehicle type as returned in vehicle model responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None


class VehicleModel(BaseModel):
    """Vehicle model as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    object_type: str | None = None
    name: str | None = None
    brand: str | None = None
    molicar_code: str | None = None
    version: str | None = None
    year_start: int | None = None
    year_end: int | None = None
    active: bool | None = None
    public_price_cents: int | None = None
    public_price_as_string: str | None = None
    publish: bool | None = None
    fipe_code: str | None = None
    public_picture: str | None = None
    vehicle_brand: VehicleBrand | None = None
    fuel: VehicleFuel | None = None
    vehicle_type: VehicleType | None = None
    created_at: str | None = None
    updated_at: str | None = None


class VehiclePriceStore(BaseModel):
    """Store as returned in vehicle price responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    display_name: str | None = None
    uf: str | None = None
    limit_vehicle_prices: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class VehiclePrice(BaseModel):
    """Vehicle price as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    store_id: int | None = None
    min_price_cents: int | None = None
    default_price_cents: int | None = None
    active: bool | None = None
    vehicle_model: VehicleModel | None = None
    store: VehiclePriceStore | None = None
    created_at: str | None = None
    updated_at: str | None = None
