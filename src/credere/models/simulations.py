"""Pydantic models for the Simulations resource."""

from __future__ import annotations

from pydantic import BaseModel


class RetrieveLead(BaseModel):
    cpf_cnpj: str


class ProductsOptions(BaseModel):
    include_capitalization_bond: bool | None = None
    include_asset_insurance: bool | None = None
    include_personal_insurance: bool | None = None


class Vehicle(BaseModel):
    vehicle_molicar_code: str
    licensing_uf: str | None = None
    licensing_city: str | None = None
    manufacture_year: int | None = None
    model_year: int | None = None
    asset_value: int | None = None
    zero_km: bool | None = None


class Condition(BaseModel):
    installments: int
    down_payment: int
    bank_febraban_code: str | None = None
    products_options: ProductsOptions | None = None
    include_financial_protection_insurance: bool | None = None
    process_credere_suggested_conditions: bool | None = None
    max_return: int | None = None
    min_return: int | None = None
    return_preference: str | None = None
    quota_preference: str | None = None


class SimulationData(BaseModel):
    process_bank_suggested_conditions: bool = True
    process_credere_suggested_conditions: bool = True
    seller_cpf: str
    retrieve_lead: RetrieveLead | None = None
    bank_febraban_codes: list[str] | None = None
    documentation_value: int | None = None
    accessory_value: int | None = None
    insurance_value: int | None = None
    commercial: bool | None = None
    vehicle: Vehicle | None = None
    conditions: list[Condition] | None = None


class SimulationResponse(BaseModel):
    simulation_id: str
    raw_response: dict
