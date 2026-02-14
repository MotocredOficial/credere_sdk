"""Authentication handling for the Credere API."""

from __future__ import annotations

import httpx


class APIKeyAuth(httpx.Auth):
    """Injects the API key as a Bearer token into every request."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def auth_flow(self, request: httpx.Request):  # type: ignore[override]
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        yield request
