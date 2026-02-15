"""Pydantic models for the Proposal Attempts resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ProposalAttemptCreateRequest(BaseModel):
    """Input model for creating or updating a proposal attempt."""

    model_config = ConfigDict(extra="allow")


class ProposalAttempt(BaseModel):
    """Proposal attempt as returned by the API."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
