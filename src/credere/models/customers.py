"""Pydantic models for the Customers resource."""

from __future__ import annotations

from pydantic import BaseModel


class BankValidations(BaseModel):
    bank_codes: list[str] | None = None
    store_id: int | None = None


class Phone(BaseModel):
    id: int | None = None
    code: int | None = None
    number: int | None = None
    phone_type_id: int | None = None
    phone_confirmation_id: int | None = None


class Accountant(BaseModel):
    id: int | None = None
    name: str | None = None
    city: str | None = None
    phone: Phone | None = None


class Address(BaseModel):
    id: int | None = None
    address_type_id: int | None = None
    city: str | None = None
    number: str | None = None
    street: str | None = None
    zip_code: str | None = None
    complement: str | None = None
    state_id: int | None = None
    neighborhood: str | None = None
    set_time_year: int | None = None
    set_time_month: int | None = None
    build_type_id: int | None = None
    rent_value_cents: int | None = None


class Email(BaseModel):
    id: int | None = None
    address: str | None = None


class BankReference(BaseModel):
    id: int | None = None
    bank_id: int | None = None
    overdraft: bool | None = None
    agency: str | None = None
    open_at: str | None = None
    account_number: str | None = None
    digit: str | None = None


class JobReference(BaseModel):
    id: int | None = None
    address: Address | None = None
    joined_at: str | None = None
    income_cents: int | None = None
    another_income_cents: int | None = None
    another_income_type_id: int | None = None
    detail: str | None = None
    first_job: bool | None = None
    professional_ocupation_id: int | None = None
    profession_id: int | None = None
    department: str | None = None
    name: str | None = None
    cnpj: str | None = None
    company_activity_id: int | None = None
    phone: Phone | None = None
    previous_work: str | None = None
    previous_work_start_at: str | None = None
    previous_work_end_at: str | None = None
    previous_job_phone: Phone | None = None


class PersonalReference(BaseModel):
    id: int | None = None
    name: str | None = None
    city: str | None = None
    phone: Phone | None = None
    relationship: str | None = None


class CustomerData(BaseModel):
    id: int | None = None
    cpf: str | None = None
    name: str | None = None
    nickname: str | None = None
    born_at: str | None = None
    have_bank_account: bool | None = None
    accountant: Accountant | None = None
    address: Address | None = None
    has_made_funding: bool | None = None
    previous_funding_bank_id: int | None = None
    accept_boleto: bool | None = None
    note: str | None = None
    emails: list[Email] | None = None
    phones: list[Phone] | None = None
    bank_references: list[BankReference] | None = None
    addresses: list[Address] | None = None
    attachments: list | None = None
    mother: str | None = None
    father: str | None = None
    document_type: str | None = None
    rg: str | None = None
    rg_date: str | None = None
    rg_state_id: int | None = None
    rg_issuing: str | None = None
    has_cnh: bool | None = None
    cnh: str | None = None
    cnh_type_id: int | None = None
    marital_status_id: int | None = None
    spouse_name: str | None = None
    spouse_born_at: str | None = None
    spouse_cpf: str | None = None
    nationality: str | None = None
    place_of_birth: str | None = None
    state_of_birth_id: int | None = None
    genre_id: int | None = None
    education_id: int | None = None
    property: int | None = None
    public_person: bool | None = None
    job_reference: JobReference | None = None
    have_credit_card: bool | None = None
    credit_cards: str | None = None
    personal_references: list[PersonalReference] | None = None


class RootModel(BaseModel):
    bank_validations: BankValidations | None = None
    customer: CustomerData | None = None


class CustomerResponse(BaseModel):
    object_type: str
    id: int
    name: str
    cpf: str
    raw_response: dict
