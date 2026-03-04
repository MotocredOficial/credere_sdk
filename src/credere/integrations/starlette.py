"""Starlette / FastAPI integration helpers for the Credere SDK.

Why a pure ASGI middleware instead of BaseHTTPMiddleware
--------------------------------------------------------
Starlette's ``BaseHTTPMiddleware`` runs the request handler inside an
``anyio`` task group.  When the handler (or any downstream middleware) raises
an exception, anyio collects it into an ``ExceptionGroup`` before
``collapse_excgroups()`` can unwrap it.  Third-party middlewares (e.g. Sentry)
that call ``await call_next(request)`` inside a bare ``try/except`` block
therefore receive an ``ExceptionGroup`` instead of the original exception,
causing the confusing double-traceback shown below::

    ExceptionGroup: unhandled errors in a TaskGroup
      + ValidationError: 1 validation error for ...
          address
            Error extracting attribute: MissingGreenlet: ...

``CredereMiddleware`` is implemented as a **pure ASGI middleware** — it never
creates its own task group, so exceptions always propagate as-is and are
visible to every upstream middleware without wrapping.

Usage with FastAPI
------------------
::

    from contextlib import asynccontextmanager
    from fastapi import FastAPI, Request
    from credere.integrations.starlette import CredereMiddleware, get_credere_client

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with AsyncCredereClient(api_key="sk-...") as client:
            app.state.credere_client = client
            yield

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(CredereMiddleware, api_key="sk-...")

    @app.get("/customers/{id}")
    async def get_customer(request: Request, id: int):
        client = get_credere_client(request)
        return await client.customers.get(id)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from credere.client import AsyncCredereClient

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.types import ASGIApp, Receive, Scope, Send

_STATE_KEY = "credere_client"


class CredereMiddleware:
    """Pure ASGI middleware that attaches an :class:`AsyncCredereClient` to
    every request's ``scope["state"]``.

    Because this is a **pure ASGI middleware** (not a subclass of
    ``BaseHTTPMiddleware``), it does **not** create an anyio task group.
    Exceptions raised by downstream code therefore propagate as ordinary
    Python exceptions — they are never silently wrapped inside an
    ``ExceptionGroup``, which means Sentry and other monitoring middlewares
    receive the original exception with a clean, readable traceback.

    Parameters
    ----------
    app:
        The next ASGI application in the middleware stack.
    api_key:
        Credere API key passed to :class:`AsyncCredereClient`.
    base_url:
        Override the default Credere API base URL.
    timeout:
        HTTP request timeout in seconds (default ``30.0``).
    store_id:
        Default store ID attached to every request (can be overridden
        per-call on the resource methods).
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        api_key: str,
        base_url: str = "https://api.credere.com",
        timeout: float = 30.0,
        store_id: int | None = None,
    ) -> None:
        self._app = app
        self._client = AsyncCredereClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            store_id=store_id,
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            if "state" not in scope:
                scope["state"] = {}
            scope["state"][_STATE_KEY] = self._client

        await self._app(scope, receive, send)

    async def close(self) -> None:
        """Close the underlying :class:`AsyncCredereClient`.

        Call this during application shutdown (e.g. inside a FastAPI
        ``lifespan`` context manager) to release the underlying
        ``httpx.AsyncClient`` connection pool.
        """
        await self._client.close()


def get_credere_client(request: Request) -> AsyncCredereClient:
    """Retrieve the :class:`AsyncCredereClient` stored by :class:`CredereMiddleware`.

    Parameters
    ----------
    request:
        The current Starlette / FastAPI ``Request`` object.

    Returns
    -------
    AsyncCredereClient
        The shared client instance attached to this request.

    Raises
    ------
    RuntimeError
        If :class:`CredereMiddleware` has not been added to the middleware
        stack before this helper is called.
    """
    try:
        return request.state.credere_client  # type: ignore[no-any-return]
    except AttributeError:
        raise RuntimeError(
            "CredereMiddleware is not installed. "
            "Add it to your ASGI app with "
            "app.add_middleware(CredereMiddleware, api_key=...)."
        ) from None
