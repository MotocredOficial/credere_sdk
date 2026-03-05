"""Pydantic models for the Leads resource."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class Address(BaseModel):
    """Address input for lead create/update requests."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None  # Exists only in the response
    zip_code: str | None = None
    city: str | None = None
    state: str | None = None
    district: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None


class DomainValue(BaseModel):
    """Domain value used for gender, occupation, profession."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    type: str | None = None
    credere_identifier: str | None = None
    label: str | None = None


class LeadData(BaseModel):
    """Input model for creating or updating a lead."""

    model_config = ConfigDict(extra="allow")

    cpf_cnpj: str | None = None
    name: str | None = None
    birthdate: str | None = None
    email: str | None = None
    has_cnh: bool | None = None
    retrieve_gender: str | None = None
    phone_number: str | None = None
    monthly_income: int | None = None
    retrieve_occupation: str | None = None
    retrieve_profession: str | None = None
    address: Address | None = None


class LeadResponse(BaseModel):
    """Lead as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    cpf_cnpj: str | None = None
    name: str | None = None
    birthdate: str | None = None
    monthly_income: int | None = None
    phone_number: str | None = None
    payload: dict[str, Any] | None = None
    gender: DomainValue | None = None
    occupation: DomainValue | None = None
    profession: DomainValue | None = None
    mother_name: str | None = None
    address: Address | None = None


class LeadRequiredFields(BaseModel):
    """Response from the required_fields endpoint."""

    model_config = ConfigDict(extra="allow")

    lead: LeadResponse | None = None
    requirements: dict[str, Any] | None = None
