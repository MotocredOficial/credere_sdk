"""Pydantic models for the Utilities resource."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Domain(BaseModel):
    """Domain value used for client and lead domains."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    type: str | None = None
    credere_identifier: str | None = None
    label: str | None = None
