"""SDK exception hierarchy."""

from __future__ import annotations


class CredereError(Exception):
    """Base exception for all Credere SDK errors."""


class CredereAPIError(CredereError):
    """The API returned an error response (4xx / 5xx)."""

    def __init__(
        self,
        status_code: int,
        message: str,
        body: dict | None = None,
    ) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(message)


class AuthenticationError(CredereAPIError):
    """401 — invalid or missing API key."""


class NotFoundError(CredereAPIError):
    """404 — resource not found."""


class CredereConnectionError(CredereError):
    """Network-level failure (DNS, connection refused, etc.)."""


class CredereTimeoutError(CredereError):
    """Request timed out."""
