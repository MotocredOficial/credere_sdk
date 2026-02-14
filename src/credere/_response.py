"""Shared response handling for all resources."""

from __future__ import annotations

import httpx

from credere.exceptions import (
    AuthenticationError,
    CredereAPIError,
    CredereConnectionError,
    CredereTimeoutError,
    NotFoundError,
)


def _parse_error_body(response: httpx.Response) -> tuple[str, dict | None]:
    """Extract an error message and body from the response."""
    try:
        body = response.json()
    except Exception:
        return response.text or f"HTTP {response.status_code}", None

    if isinstance(body, dict):
        error = body.get("error", {})
        if isinstance(error, dict):
            message = error.get("message", response.text)
        else:
            message = body.get("message", response.text)
        return message, body

    return response.text or f"HTTP {response.status_code}", None


def raise_for_status(response: httpx.Response) -> None:
    """Raise an SDK exception if the response is an error.

    Maps:
        401 → AuthenticationError
        404 → NotFoundError
        other 4xx/5xx → CredereAPIError
    """
    if response.is_success:
        return

    message, body = _parse_error_body(response)
    status = response.status_code

    if status == 401:
        raise AuthenticationError(status, message, body)
    if status == 404:
        raise NotFoundError(status, message, body)
    raise CredereAPIError(status, message, body)


def handle_request_error(exc: httpx.HTTPError) -> None:
    """Wrap httpx transport errors into SDK exceptions."""
    if isinstance(exc, httpx.TimeoutException):
        raise CredereTimeoutError(str(exc)) from exc
    if isinstance(exc, httpx.ConnectError):
        raise CredereConnectionError(str(exc)) from exc
    raise CredereConnectionError(str(exc)) from exc
