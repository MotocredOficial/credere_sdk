"""Pydantic models for the Proposals resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from credere.models.simulations import Bank


class ProposalConditionRequest(BaseModel):
    """Input condition for a proposal request."""

    model_config = ConfigDict(extra="allow")

    down_payment: int
    financed_amount: int
    installments: int


class ProposalVehicleRequest(BaseModel):
    """Input vehicle for a proposal request."""

    model_config = ConfigDict(extra="allow")

    asset_value: int
    licensing_uf: str
    manufacture_year: int
    model_year: int
    vehicle_molicar_code: str
    zero_km: bool


class ProposalCreateRequest(BaseModel):
    """Top-level input for creating a proposal."""

    model_config = ConfigDict(extra="allow")

    assets_value: int
    documentation_value: int | None = None
    conditions: list[ProposalConditionRequest]
    retrieve_lead: dict[str, str]
    seller_cpf: str
    vehicle: ProposalVehicleRequest


class ProposalCondition(BaseModel):
    """Condition as returned in proposal responses."""

    model_config = ConfigDict(extra="allow")

    installments: int | None = None
    down_payment: int | None = None
    financed_amount: int | None = None
    bank: Bank | None = None
    interest_monthly: float | None = None
    cet_monthly: float | None = None
    cet_annually: float | None = None


class ProposalVehicle(BaseModel):
    """Vehicle as returned in proposal responses."""

    model_config = ConfigDict(extra="allow")

    asset_value: int | None = None
    licensing_uf: str | None = None
    manufacture_year: int | None = None
    model_year: int | None = None
    vehicle_molicar_code: str | None = None
    zero_km: bool | None = None


class Proposal(BaseModel):
    """Proposal as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    assets_value: int | None = None
    documentation_value: int | None = None
    conditions: list[ProposalCondition] | None = None
    vehicle: ProposalVehicle | None = None
    retrieve_lead: dict | None = None
    seller_cpf: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
