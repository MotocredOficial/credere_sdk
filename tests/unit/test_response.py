"""Tests for _response.py — error parsing, status mapping, and transport errors.

Every test here calls the actual functions with real httpx objects.
No mocks, no patches — just input → output assertions.
"""

import httpx
import pytest

from credere._response import _parse_error_body, handle_request_error, raise_for_status
from credere.exceptions import (
    AuthenticationError,
    CredereAPIError,
    CredereConnectionError,
    CredereTimeoutError,
    NotFoundError,
)

# ---------------------------------------------------------------------------
# _parse_error_body
# ---------------------------------------------------------------------------


class TestParseErrorBody:
    def test_nested_error_dict_extracts_message(self) -> None:
        response = httpx.Response(
            400,
            json={"error": {"message": "field X is required", "status": 400}},
        )
        message, body = _parse_error_body(response)

        assert message == "field X is required"
        assert body == {"error": {"message": "field X is required", "status": 400}}

    def test_error_key_is_string_falls_back_to_body_message(self) -> None:
        """When 'error' is not a dict, uses body['message'] instead."""
        response = httpx.Response(
            400,
            json={"error": "bad_request", "message": "Something went wrong"},
        )
        message, body = _parse_error_body(response)

        assert message == "Something went wrong"
        assert body["error"] == "bad_request"

    def test_error_key_is_string_no_message_falls_back_to_text(self) -> None:
        """When 'error' is not a dict and no 'message' key, uses response text."""
        response = httpx.Response(
            400,
            json={"error": "bad_request"},
        )
        message, body = _parse_error_body(response)

        # response.text is the JSON-encoded body as a string
        assert message == response.text
        assert body == {"error": "bad_request"}

    def test_non_json_response_returns_text(self) -> None:
        response = httpx.Response(500, text="Internal Server Error")
        message, body = _parse_error_body(response)

        assert message == "Internal Server Error"
        assert body is None

    def test_non_json_empty_response_returns_status_placeholder(self) -> None:
        response = httpx.Response(502, text="")
        message, body = _parse_error_body(response)

        assert message == "HTTP 502"
        assert body is None

    def test_json_body_is_list_returns_text(self) -> None:
        """JSON that parses to a list (not dict) hits the fallback."""
        response = httpx.Response(400, json=["error1", "error2"])
        message, body = _parse_error_body(response)

        assert message == response.text
        assert body is None

    def test_json_body_is_number_returns_text(self) -> None:
        response = httpx.Response(400, json=42)
        message, body = _parse_error_body(response)

        assert message == response.text
        assert body is None


# ---------------------------------------------------------------------------
# raise_for_status
# ---------------------------------------------------------------------------


class TestRaiseForStatus:
    def test_success_returns_none(self) -> None:
        response = httpx.Response(200, json={"ok": True})
        result = raise_for_status(response)
        assert result is None

    def test_201_returns_none(self) -> None:
        response = httpx.Response(201, json={"created": True})
        assert raise_for_status(response) is None

    def test_401_raises_authentication_error(self) -> None:
        response = httpx.Response(401, json={"error": {"message": "Invalid API key"}})
        with pytest.raises(AuthenticationError) as exc_info:
            raise_for_status(response)

        assert exc_info.value.status_code == 401
        assert str(exc_info.value) == "Invalid API key"
        assert exc_info.value.body == {"error": {"message": "Invalid API key"}}

    def test_404_raises_not_found_error(self) -> None:
        response = httpx.Response(
            404, json={"error": {"message": "Customer not found"}}
        )
        with pytest.raises(NotFoundError) as exc_info:
            raise_for_status(response)

        assert exc_info.value.status_code == 404
        assert str(exc_info.value) == "Customer not found"

    def test_422_raises_credere_api_error(self) -> None:
        response = httpx.Response(422, json={"error": {"message": "Validation failed"}})
        with pytest.raises(CredereAPIError) as exc_info:
            raise_for_status(response)

        assert exc_info.value.status_code == 422
        assert str(exc_info.value) == "Validation failed"

    def test_500_with_plain_text_raises_credere_api_error(self) -> None:
        response = httpx.Response(500, text="Internal Server Error")
        with pytest.raises(CredereAPIError) as exc_info:
            raise_for_status(response)

        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Internal Server Error"
        assert exc_info.value.body is None

    def test_error_body_is_preserved(self) -> None:
        body = {"error": {"message": "bad", "code": "INVALID"}, "request_id": "abc"}
        response = httpx.Response(400, json=body)
        with pytest.raises(CredereAPIError) as exc_info:
            raise_for_status(response)

        assert exc_info.value.body == body


# ---------------------------------------------------------------------------
# handle_request_error
# ---------------------------------------------------------------------------


class TestHandleRequestError:
    def test_timeout_raises_credere_timeout_error(self) -> None:
        request = httpx.Request("GET", "https://api.example.com/test")
        exc = httpx.TimeoutException("connection timed out", request=request)

        with pytest.raises(CredereTimeoutError) as exc_info:
            handle_request_error(exc)

        assert str(exc_info.value) == "connection timed out"
        assert exc_info.value.__cause__ is exc

    def test_connect_error_raises_credere_connection_error(self) -> None:
        request = httpx.Request("POST", "https://api.example.com/test")
        exc = httpx.ConnectError("connection refused", request=request)

        with pytest.raises(CredereConnectionError) as exc_info:
            handle_request_error(exc)

        assert str(exc_info.value) == "connection refused"
        assert exc_info.value.__cause__ is exc

    def test_other_transport_error_raises_credere_connection_error(self) -> None:
        """Non-timeout, non-connect errors also become
        CredereConnectionError."""
        request = httpx.Request("GET", "https://api.example.com/test")
        exc = httpx.ReadError("connection reset by peer", request=request)

        with pytest.raises(CredereConnectionError) as exc_info:
            handle_request_error(exc)

        assert str(exc_info.value) == "connection reset by peer"
        assert exc_info.value.__cause__ is exc

    def test_read_timeout_is_a_timeout_exception(self) -> None:
        """ReadTimeout is a TimeoutException subclass —
        should raise CredereTimeoutError."""
        request = httpx.Request("GET", "https://api.example.com/test")
        exc = httpx.ReadTimeout("read timed out", request=request)

        with pytest.raises(CredereTimeoutError) as exc_info:
            handle_request_error(exc)

        assert str(exc_info.value) == "read timed out"


# ---------------------------------------------------------------------------
# _headers logic (tested via resource class, no HTTP involved)
# ---------------------------------------------------------------------------


class TestHeadersLogic:
    """Test _headers() directly — this is pure logic, no network."""

    def test_headers_with_store_id_from_constructor(self) -> None:
        from credere.resources.customers import Customers

        # Pass a real httpx.Client but we never make a request
        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Customers(client, store_id=42)
            headers = resource._headers()

            assert headers == {"Store-Id": "42"}
        finally:
            client.close()

    def test_headers_with_store_id_override(self) -> None:
        from credere.resources.customers import Customers

        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Customers(client, store_id=42)
            headers = resource._headers(store_id=99)

            assert headers == {"Store-Id": "99"}
        finally:
            client.close()

    def test_headers_without_store_id_returns_empty(self) -> None:
        from credere.resources.customers import Customers

        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Customers(client, store_id=None)
            headers = resource._headers()

            assert headers == {}
        finally:
            client.close()

    def test_headers_zero_store_id_is_valid(self) -> None:
        """store_id=0 should produce a header, not be treated as None."""
        from credere.resources.customers import Customers

        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Customers(client, store_id=0)
            headers = resource._headers()

            assert headers == {"Store-Id": "0"}
        finally:
            client.close()

    def test_leads_headers_include_accept_json(self) -> None:
        """Leads._headers adds Accept: application/json when store_id is set."""
        from credere.resources.leads import Leads

        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Leads(client, store_id=1)
            headers = resource._headers()

            assert headers == {"Store-Id": "1", "Accept": "application/json"}
        finally:
            client.close()

    def test_leads_headers_without_store_id_returns_empty(self) -> None:
        from credere.resources.leads import Leads

        client = httpx.Client(base_url="https://test.example.com")
        try:
            resource = Leads(client, store_id=None)
            headers = resource._headers()

            assert headers == {}
        finally:
            client.close()
