"""Pydantic models for the Proposals resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ProposalAttempt(BaseModel):
    simulation_condition_id: int
    external_simulation_uuid: str


class ProposalData(BaseModel):
    model_config = ConfigDict(extra="allow")

    customer_id: int
    store_id: int
    seller_id: int
    commercial: bool

    proposal_attemps: list[ProposalAttempt]

    km_mileage: int | None = None
    license_plate_code: str | None = None
    renavam_code: str | None = None
    chassi_code: str | None = None
    color: str | None = None
    licensing_uf: str | None = None
    licensing_city: str | None = None


class ProposalResponse(BaseModel):
    object_type: str
    id: int
    raw_response: dict
