"""Pydantic models for the Proposal Attempts resource."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProposalAttemptRequest(BaseModel):
    simulation_condition_id: int
    external_simulation_uuid: str


class ProposalAttemptCreateRequest(BaseModel):
    proposal_id: int
    proposal_attempt: ProposalAttemptRequest


class ProposalAttemptUpdateRequest(ProposalAttemptCreateRequest):
    pass


class Bank(BaseModel):
    id: int
    name: str
    tradename: str
    febraban_code: str


class Plan(BaseModel):
    return_field: str | None = Field(alias="return")

    model_config = {"populate_by_name": True}


class Table(BaseModel):
    description: str | None = None


class FundingType(BaseModel):
    id: int
    name: str


class PaymentType(BaseModel):
    id: int
    name: str


class Application(BaseModel):
    id: int
    name: str


class ExpenseInfo(BaseModel):
    object_type: str
    id: int
    created_at: datetime
    updated_at: datetime
    value_in_cents: int
    credere_type: str
    description: str | None = None
    expense: str | None = None


class PaymentFlowItem(BaseModel):
    installment_number: int
    value_cents: int


class ProposalAttemptResponse(BaseModel):
    object_type: str
    id: int
    created_at: datetime
    updated_at: datetime
    active: bool

    bank: Bank
    input_financing_in_cents: int
    plan: Plan
    quota_in_cents: int
    state: str
    table: Table
    term_financing: int
    value_in_cents: int
    obs: str | None = None
    value_of_the_license_plate_in_cents: int
    financed_amount_in_cents: int
    coefficient: float | None = None
    has_license_plate: bool
    first_payment_in_days: int

    funding_type: FundingType
    payment_type: PaymentType
    input_origin: int
    application: Application

    external_simulation_uuid: str | None = None
    simulation_condition_id: int | None = None
    external_proposal_uuid: str | None = None
    state_rank: int
    bank_proposal_identifier: str | None = None
    honda_id: str | None = None
    simulation_pre_approval_status: int | None = None
    fixed_installments: bool
    cet_monthly: float | None = None
    cet_annually: float | None = None
    return_value_cents: int | None = None
    formalization_state: str | None = None
    formalization: dict | None = None
    replaced_by_proposal_attempt_id: int | None = None
    replaces_proposal_attempt_id: int | None = None
    has_accessory: bool
    value_of_the_accessory_in_cents: int

    expenses: list[ExpenseInfo]
    payment_flow: list[PaymentFlowItem]
