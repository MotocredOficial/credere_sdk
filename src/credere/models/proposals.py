"""Pydantic models for the Proposals resource."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from credere.models.simulations import Bank


class ProposalAttempt(BaseModel):
    simulation_condition_id: int
    external_simulation_uuid: str


class ProposalData(BaseModel):
    model_config = ConfigDict(extra="allow")

    customer_id: int
    store_id: int
    seller_id: int
    commercial: bool

    proposal_attempts: list[ProposalAttempt]

    km_mileage: int | None = None
    license_plate_code: str | None = None
    renavam_codes: str | None = None
    chasse_code: str | None = None
    color: str | None = None
    licensing_uf: str | None = None
    licensing_city: str | None = None


class ProposalCreateRequest(BaseModel):
    """Top-level input for creating a proposal."""

    proposal: ProposalData


class ProposalUpdateRequest(BaseModel):
    """Top-level input for updating a proposal."""

    model_config = ConfigDict(extra="allow")

    id: int

    proposal: ProposalData


class Phone(BaseModel):
    code: int
    number: int


class Customer(BaseModel):
    id: int
    name: str
    cpf: str | None = None
    cnpj: str | None = None
    born_at: date
    phones: list[Phone]


class Seller(BaseModel):
    id: int
    name: str


class Store(BaseModel):
    id: int
    name: str
    seller_can_send_proposal_to_bank: bool


class Plan(BaseModel):
    return_field: str  # "return" is reserved keyword
    return_offset: str | None = None

    model_config = ConfigDict(populate_by_name=True)

    # alias to match JSON
    return_field: str = Field(alias="return")


class Table(BaseModel):
    description: str


class FundingType(BaseModel):
    id: int
    name: str


class PaymentType(BaseModel):
    id: int
    name: str


class Application(BaseModel):
    id: int
    name: str


class IntegrationError(BaseModel):
    error: str
    message: str
    error_details: str


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


# ---- Proposal Attempt ----


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
    external_simulation_uuid: str
    simulation_condition_id: int
    external_proposal_uuid: str
    integration_error: IntegrationError
    state_rank: int
    bank_proposal_identifier: str
    honda_id: str
    simulation_pre_approval_status: int
    fixed_installments: bool
    cet_monthly: float
    cet_annually: float
    return_value_cents: int | None = None
    formalization_state: str | None = None
    formalization: str | None = None
    replaced_by_proposal_attempt_id: int | None = None
    replaces_proposal_attempt_id: int | None = None
    has_accessory: bool
    value_of_the_accessory_in_cents: int

    expenses: list[ExpenseInfo]
    payment_flow: list[PaymentFlowItem]


# ---- Vehicle / Fuel ----


class VehicleBrand(BaseModel):
    id: int
    name: str


class Fuel(BaseModel):
    object_type: str
    id: int
    created_at: datetime
    updated_at: datetime
    name: str


class VehicleType(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    honda_code: str


class VehicleModel(BaseModel):
    object_type: str
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    brand: str
    molicar_code: str
    version: str
    year_end: int
    year_start: int
    active: bool
    public_price_cents: int
    public_price_as_string: str
    publish: bool
    fipe_code: str
    public_picture: str | None = None

    vehicle_brand: VehicleBrand
    fuel: Fuel
    vehicle_type: VehicleType


# ---- Main Proposal ----


class ProposalCreateResponse(BaseModel):
    object_type: str
    id: int
    created_at: datetime
    updated_at: datetime

    customer: Customer
    seller: Seller
    state: str
    store: Store

    year_of_model: int
    year_of_manufacture: int
    comments_count: int
    external_simulation_uuid: str
    sent_to_bank: bool
    zero_km: bool
    commercial: bool
    creation_external_link_id: int | None = None

    licensing_uf: str | None = None
    licensing_city: str | None = None
    chassi_code: str | None = None
    license_plate_code: str | None = None
    renavam_code: str | None = None
    km_mileage: int | None = None
    color: str | None = None

    proposal_attempt: ProposalAttemptResponse
    vehicle_model: VehicleModel
    fuel: Fuel


class ProposalGetResponse(BaseModel):
    proposal: ProposalCreateResponse


class ProposalListResponse(BaseModel):
    proposals: list[ProposalCreateResponse]
