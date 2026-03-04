"""Pydantic models for the Bank Credentials resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Bank(BaseModel):
    """Bank as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    febraban_code: str | None = None
    name: str | None = None


class IntegratedBank(BaseModel):
    """Integrated bank as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    store_id: int | None = None
    bank: Bank | None = None
    credentials_status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
