"""Pydantic models for the Plus Returns resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PlusReturnRuleCreateRequest(BaseModel):
    """Input model for creating or updating a plus return rule."""

    model_config = ConfigDict(extra="allow")


class PlusReturnRule(BaseModel):
    """Plus return rule as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
