"""Pydantic models for the Simulations resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SimulationConditionRequest(BaseModel):
    """Input condition for a simulation request."""

    model_config = ConfigDict(extra="allow")

    down_payment: int
    financed_amount: int
    installments: int


class SimulationVehicleRequest(BaseModel):
    """Input vehicle for a simulation request."""

    model_config = ConfigDict(extra="allow")

    asset_value: int
    licensing_uf: str
    manufacture_year: int
    model_year: int
    vehicle_molicar_code: str
    zero_km: bool


class SimulationCreateRequest(BaseModel):
    """Top-level input for creating a simulation."""

    model_config = ConfigDict(extra="allow")

    assets_value: int
    documentation_value: int | None = None
    conditions: list[SimulationConditionRequest]
    retrieve_lead: dict[str, str]
    seller_cpf: str
    vehicle: SimulationVehicleRequest


class Bank(BaseModel):
    """Bank as returned in simulation condition responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    febraban_code: str | None = None
    name: str | None = None
    nickname: str | None = None


class SimulationCondition(BaseModel):
    """Condition as returned in simulation responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    installments: int | None = None
    down_payment: int | None = None
    financed_amount: int | None = None
    created_at: str | None = None
    bank: Bank | None = None
    success: bool | None = None
    error: str | None = None
    interest_monthly: float | None = None
    interest_annually: float | None = None
    cet_monthly: float | None = None
    cet_annually: float | None = None
    first_installment_value: int | None = None
    last_installment_value: int | None = None
    amount_paid_in_financing: int | None = None
    available: bool | None = None
    credit_condition_code: str | None = None
    credit_condition_description: str | None = None
    process_task: dict | None = None
    pre_approval_status: str | None = None
    reason: str | None = None


class Simulation(BaseModel):
    """Simulation as returned by the API."""

    model_config = ConfigDict(extra="allow")

    assets_value: int | None = None
    conditions: list[SimulationCondition] | None = None
