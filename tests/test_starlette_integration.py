"""Tests for the Starlette/ASGI integration middleware.

These tests verify two properties that are critical for production use:

1. **Client lifecycle** - ``CredereMiddleware`` attaches an
   ``AsyncCredereClient`` to every request scope, so route handlers can
   retrieve it with ``get_credere_client(request)``.

2. **Exception transparency** - because ``CredereMiddleware`` is a *pure ASGI*
   middleware (not a ``BaseHTTPMiddleware`` subclass), exceptions raised by
   downstream handlers propagate as regular Python exceptions and are **never**
   wrapped inside ``ExceptionGroup``.

   The original error that motivated this integration looked like::

       ExceptionGroup: unhandled errors in a TaskGroup
         + ValidationError: 1 validation error for CustomerDomain
             address
               Error extracting attribute: MissingGreenlet: ...

   ``BaseHTTPMiddleware`` creates an anyio task group for each request; when
   an exception escapes the handler, anyio boxes it in an ``ExceptionGroup``
   before ``collapse_excgroups()`` gets a chance to unwrap it.  Sentry-style
   middlewares that simply ``await call_next(request)`` inside a plain
   ``try/except`` then see the group instead of the real exception.

   ``CredereMiddleware`` avoids the task group entirely, so the exception
   surfaces directly.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from credere.client import AsyncCredereClient
from credere.integrations.starlette import CredereMiddleware, get_credere_client

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

API_KEY = "sk-test"
BASE_URL = "https://api.credere.com"
CUSTOMERS_URL = f"{BASE_URL}/v1/customers"

SAMPLE_CUSTOMER = {
    "customer": {
        "id": 7,
        "object_type": "Customer",
        "cpf_cnpj": "12345678901",
        "name": "Joao Silva",
        "email": "joao@example.com",
        "birthdate": "1990-01-15",
        "phone_number": "11999990000",
        "gender": None,
        "profession": None,
        "occupation": None,
        "monthly_income": 500000,
        "mother_name": None,
        "address": {
            "id": 1,
            "zip_code": "01310100",
            "street": "Av. Paulista",
            "number": "900",
            "complement": None,
            "district": "Bela Vista",
            "city": "Sao Paulo",
            "state": "SP",
        },
        "active": True,
        "created_at": "2024-01-01T00:00:00-03:00",
        "updated_at": "2024-01-01T00:00:00-03:00",
    }
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def build_app(*, raise_in_handler: bool = False) -> Starlette:
    """Build a minimal Starlette app with ``CredereMiddleware``."""

    async def get_customer(request: Request) -> JSONResponse:
        if raise_in_handler:
            raise ValueError("deliberate error")

        client = get_credere_client(request)
        customer = await client.customers.get(7)
        return JSONResponse({"id": customer.id, "name": customer.name})

    async def healthcheck(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    app = Starlette(
        routes=[
            Route("/customers/{id:int}", get_customer),
            Route("/health", healthcheck),
        ]
    )
    app.add_middleware(
        CredereMiddleware,
        api_key=API_KEY,
        base_url=BASE_URL,
    )
    return app


# ---------------------------------------------------------------------------
# Tests - client attachment
# ---------------------------------------------------------------------------


class TestCredereMiddlewareClientAttachment:
    @respx.mock
    def test_client_is_attached_to_request_state(self) -> None:
        """get_credere_client() returns the shared AsyncCredereClient."""
        respx.get(f"{CUSTOMERS_URL}/7").mock(
            return_value=httpx.Response(200, json=SAMPLE_CUSTOMER)
        )

        app = build_app()
        with TestClient(app, raise_server_exceptions=True) as client:
            response = client.get("/customers/7")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 7
        assert data["name"] == "Joao Silva"

    def test_non_http_scope_does_not_crash(self) -> None:
        """Middleware handles a lifespan scope without raising."""
        app = build_app()
        # TestClient exercises the lifespan scope internally; just starting and
        # stopping the client is sufficient to confirm no crash.
        with TestClient(app):
            pass

    def test_healthcheck_does_not_require_credere_client(self) -> None:
        """Routes that don't call get_credere_client() work fine."""
        app = build_app()
        with TestClient(app) as client:
            response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Tests - exception transparency (the core motivation for pure-ASGI approach)
# ---------------------------------------------------------------------------


class TestExceptionTransparency:
    def test_exception_propagates_as_plain_exception_not_exception_group(
        self,
    ) -> None:
        """Exceptions from handlers are NOT wrapped in ExceptionGroup.

        This is the key difference from BaseHTTPMiddleware: the pure-ASGI
        implementation never creates an anyio task group, so exceptions always
        surface as their original type.
        """
        app = build_app(raise_in_handler=True)

        with TestClient(app, raise_server_exceptions=True) as client, pytest.raises(
            ValueError, match="deliberate error"
        ):
            client.get("/customers/1")

    def test_exception_is_not_an_exception_group(self) -> None:
        """The raised exception is not wrapped in ExceptionGroup."""
        app = build_app(raise_in_handler=True)

        with TestClient(app, raise_server_exceptions=True) as client:
            try:
                client.get("/customers/1")
            except Exception as exc:
                # Must be the raw ValueError, not an ExceptionGroup
                assert not isinstance(exc, ExceptionGroup), (
                    "Exception was wrapped in ExceptionGroup -- "
                    "this is the BaseHTTPMiddleware bug we are fixing."
                )
                assert isinstance(exc, ValueError)


# ---------------------------------------------------------------------------
# Tests - get_credere_client error handling
# ---------------------------------------------------------------------------


class TestGetCredereClient:
    def test_raises_runtime_error_when_middleware_not_installed(self) -> None:
        """get_credere_client() raises RuntimeError if middleware is absent."""

        async def handler(request: Request) -> JSONResponse:
            # No middleware installed, so this must raise RuntimeError.
            get_credere_client(request)
            return JSONResponse({})  # pragma: no cover

        bare_app = Starlette(routes=[Route("/", handler)])

        with (
            TestClient(bare_app, raise_server_exceptions=True) as client,
            pytest.raises(RuntimeError, match="CredereMiddleware is not installed"),
        ):
            client.get("/")


# ---------------------------------------------------------------------------
# Tests - CredereMiddleware.close()
# ---------------------------------------------------------------------------


class TestCredereMiddlewareClose:
    async def test_close_is_idempotent(self) -> None:
        """Calling close() multiple times does not raise."""
        middleware = CredereMiddleware(
            app=lambda s, r, snd: None,  # type: ignore[arg-type]
            api_key=API_KEY,
        )
        await middleware.close()
        # Second close should not raise even though the client is already shut.
        # httpx.AsyncClient.aclose() is idempotent.
        await middleware.close()

    def test_internal_client_is_async_credere_client(self) -> None:
        middleware = CredereMiddleware(
            app=lambda s, r, snd: None,  # type: ignore[arg-type]
            api_key=API_KEY,
            store_id=5,
        )
        assert isinstance(middleware._client, AsyncCredereClient)
