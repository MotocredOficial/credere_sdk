"""Pydantic models for the Customers resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CustomerAddressRequest(BaseModel):
    """Address input for customer create/update requests."""

    model_config = ConfigDict(extra="allow")

    zip_code: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None


class CustomerAddress(BaseModel):
    """Address as returned in customer responses (includes id)."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    zip_code: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None


class CustomerCreateRequest(BaseModel):
    """Input model for creating or updating a customer."""

    model_config = ConfigDict(extra="allow")

    cpf_cnpj: str | None = None
    name: str | None = None
    birthdate: str | None = None
    email: str | None = None
    phone_number: str | None = None
    gender: str | None = None
    profession: str | None = None
    monthly_income: int | None = None
    mother_name: str | None = None
    address: CustomerAddressRequest | None = None


class Customer(BaseModel):
    """Customer as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    object_type: str | None = None
    cpf_cnpj: str | None = None
    name: str | None = None
    email: str | None = None
    birthdate: str | None = None
    phone_number: str | None = None
    gender: dict | None = None
    profession: dict | None = None
    occupation: dict | None = None
    monthly_income: int | None = None
    mother_name: str | None = None
    address: CustomerAddress | None = None
    active: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
