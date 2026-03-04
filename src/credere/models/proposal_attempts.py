"""Pydantic models for the Proposal Attempts resource."""

from __future__ import annotations

from pydantic import BaseModel


class ProposalAttemptRequest(BaseModel):
    simulation_condition_id: int
    external_simulation_uuid: str


class ProposalAttemptData(BaseModel):
    proposal_id: int
    proposal_attempt: ProposalAttemptRequest


class ProposalAttemptResponse(BaseModel):
    object_type: str
    id: int
    raw_response: dict
