# Code Review: PR #25 — `feature/working-core-for-avelloz`

> **Verdict: Request Changes** — 2 critical bugs and several high-severity issues need fixing before merge.

---

## 🔴 CRITICAL — Must fix before merge

### 1. `dict.update()` returns `None` — proposal update sends `null` body
**File:** `src/credere/resources/proposals.py` (sync & async `update()`)

```python
# BUG: dict.update() mutates in-place and returns None
json={
    "proposal": data.model_dump(exclude_none=True).update({"id": id})
}
# Sends: {"proposal": null} — will fail with 400/422 on every call
```

**Fix:**
```python
body = data.model_dump(exclude_none=True)
body["id"] = id
json={"proposal": body}
```

### 2. Typo `proposal_attemps` propagates into the API JSON key
**File:** `src/credere/models/proposals.py`

```python
class ProposalData(BaseModel):
    proposal_attemps: list[ProposalAttempt]  # missing 't' in "attempts"
```

When serialized, the key `"proposal_attemps"` is sent to the API. If the server expects `"proposal_attempts"`, every proposal create/update silently drops the attempts list. The integration tests carry the same typo so the test suite won't catch it.

---

## 🟠 HIGH — Blocking issues

### 3. `AsyncCustomers.update()` missing `bank_list` parameter
The sync `Customers.update()` accepts `bank_list: list[str]` and sends `bank_validations` in the payload. The async version is missing both parameter and payload key entirely — a direct parity bug.

### 4. `update()` response parsing missing envelope key
Both `proposals.py` and `proposal_attempts.py` `update()` methods read `response.json()` directly (expecting top-level `object_type`, `id`), while `create()` and `get()` correctly unwrap via `response.json()["proposal"]` / `response.json()["proposal_attempt"]`. This will raise a `KeyError` on any successful update response.

### 5. `ProposalAttempts.update()` sends wrong type as request body
`update()` accepts `ProposalAttemptResponse` (which contains `raw_response: dict`) instead of a data/request model. The serialized body will include the entire raw API response dict — almost certainly not what the server expects. The parameter type should be `ProposalAttemptData`.

### 6. Leading `/` on `_BASE_PATH` inconsistency

| Resource | `_BASE_PATH` |
|---|---|
| `customers.py`, `proposals.py`, `simulations.py` | `"api/v1/..."` ✅ |
| `leads.py` | `"/api/v1/banks_api/leads"` ❌ |
| `proposal_attempts.py` | `"/api/v1/proposals/{id}/proposal_attempts"` ❌ |

With httpx, a leading `/` replaces the path component of the base URL rather than appending to it. Standardize to no leading slash.

### 7. `banks()`, `vehicle_by_plate()`, `vehicle_by_chassis()` removed with no replacement
The entire `Utilities` resource is deleted. These three endpoints have no equivalent anywhere in the new code. Any avelloz code that uses vehicle lookups by plate/chassis will get `AttributeError` at runtime.

---

## 🟡 MEDIUM

### 8. `customers.domains()` missing `store_id` / headers
Unlike `leads.domains()` which passes `headers=self._headers()`, `customers.domains()` sends no headers. If the endpoint requires `Store-Id` for scoping, it won't be sent.

**Fix:** Add `store_id` parameter and pass `headers=self._headers(store_id)`.

### 9. Fragile URL construction with `str.replace()`
```python
_BASE_PATH.replace("customers", "domains")  # customers.py
_BASE_PATH.replace("leads", "domains")       # leads.py
```
Define explicit constants instead: `_DOMAINS_PATH = "api/v1/domains"`.

### 10. `python-dotenv` in production dependencies
`python-dotenv` is only used in `tests/integration/config.py`. Move it to dev/test optional dependencies — not every SDK consumer should install it.

### 11. Incompatible `Domain` model schemas
- Old `Domain` (utilities.py): `id, type, credere_identifier, label`
- New `Domain` (customers.py): `id, name, identifier`
- `DomainValue` in `leads.py` still uses the old schema

Unify or clearly name-distinguish these.

---

## 🔵 LOW / Design

### 12. `ProposalAttempt` name collision
`models/proposals.py` defines `ProposalAttempt` (an entry in a proposal's list). `models/proposal_attempts.py` defines `ProposalAttemptData`/`ProposalAttemptResponse`. Rename the one in `models/proposals.py` to `ProposalAttemptEntry` to avoid confusion at import time.

### 13. Hardcoded production IDs in integration tests
```python
CUSTOMER_ID = 2472825
SELLER_ID = 42102
SIMULATION_UUID = "1a887757-d67c-4d96-8bd2-f41756e46c56"
```
Move to environment variables, consistent with `API_KEY`.

### 14. No guard for unconfigured integration test runs
If `API_KEY == "YOUR_API_KEY_HERE"`, tests fire real HTTP requests to production. Add `pytest.skip()` in the integration conftest.

### 15. `Proposals.update()` unit test doesn't validate request body
`TestProposalsUpdate.test_update_proposal` checks `route.called` but not what was sent. The critical `None`-body bug (#1) passes undetected because `respx` intercepts regardless of body. Add a body assertion.

### 16. Module docstring accidentally deleted from `src/credere/__init__.py`

### 17. Breaking changes — no migration shims
All model names changed (e.g. `CustomerCreateRequest` → `CustomerData`), `Proposals.get_ownership()` / `leave_ownership()` deleted, `ProposalAttempts.perform_action()` deleted, default base URL changed. Any existing consumer will have every import broken. Document the breaking changes in the PR description or a `CHANGELOG` entry.

---

## Summary

| Severity | Count |
|---|---|
| 🔴 Critical | 2 |
| 🟠 High | 5 |
| 🟡 Medium | 4 |
| 🔵 Low | 6 |

Fix **#1 and #2** before anything else — they cause every proposal update/create to silently fail. Fix **#3–#6** before the async/sync parity and routing issues cause production failures.
