"""Pydantic models for the Users resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserRole(BaseModel):
    """User role as returned in user responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    identifier: str | None = None
    name: str | None = None


class UserAccount(BaseModel):
    """User account as returned in user responses."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    active: bool | None = None
    send_sms: bool | None = None
    state: str | None = None
    beta_until: str | None = None


class User(BaseModel):
    """User as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    email: str | None = None
    cpf: str | None = None
    account_name: str | None = None
    role: UserRole | None = None
    account: UserAccount | None = None
    avatar: dict | None = None
    active_alerts: dict | None = None
    created_at: str | None = None
    updated_at: str | None = None
