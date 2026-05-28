---
name: implement-api-endpoint
description: Use when adding or modifying API endpoints in smartsheet-python-sdk - implementing resource methods, handling request/response serialization, or updating endpoint parameters
---

# Implement API Endpoint

## Overview

Complete workflow for implementing SDK endpoints: resource method, model objects, serialization, comprehensive tests (5 required types), and documentation. **Implementation alone is ~20% of the work.**

**CRITICAL REQUIREMENTS:**
1. You MUST use TodoWrite to create a todo for EACH checklist item below before starting implementation
2. You MUST have OpenAPI spec for the endpoint (Smartsheet public API: https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json OR user-provided spec path)
3. Implementation MUST exactly match the spec (parameters, types, request/response structure)

## When to Use

- Adding new SDK endpoint (GET, POST, PUT, DELETE, PATCH)
- Modifying existing endpoint (parameters, return type, behavior)
- Updating endpoint for API changes

**GOLD STANDARD TEMPLATE: tests/mock_api/reports/** 
**Before implementing, review report tests as your reference implementation. Follow these patterns exactly.**

**Not done until:** All 4 components exist (code, tests, WireMock mappings, docs) AND verified against OpenAPI spec

## Core Pattern

SDK endpoints require 4 components in order:

```
1. Resource Method (smartsheet/{resource}.py)
2. Mock API Tests (tests/mock_api/{resource}/)
3. WireMock Mappings (smartsheet-sdk-tests repo)
4. Documentation (docs-source/)
```

**Implementation is NOT done until all 4 exist.**

## Implementation Checklist

**STOP: Before writing ANY code:**

1. **Obtain OpenAPI spec:**
   - Use Smartsheet public API spec: https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json
   - OR if endpoint not documented there, request spec path from user
   - **Cannot proceed without spec - ask user if not provided**

2. **Obtain WireMock mappings:**
   - Use Smartsheet SDK tests repo: https://github.com/smartsheet/smartsheet-sdk-tests
   - OR request local filesystem path from user
   - **Cannot proceed without mappings - ask user if not provided**

3. **Use TodoWrite to create a todo for EVERY checkbox below**

**Violating these rules means incomplete/incorrect work. Always verify spec and mappings first, create todos second.**

### 0. OpenAPI Spec Verification

**MUST be completed before implementation:**

- [ ] OpenAPI spec obtained (public API URL or user-provided path)
- [ ] Endpoint exists in spec with correct path
- [ ] HTTP method matches spec
- [ ] Request parameters match spec (names, types, required/optional)
- [ ] Request body schema matches spec (for POST/PUT/PATCH)
- [ ] Response schema matches spec (structure, property types)
- [ ] Error responses documented in spec
- [ ] Query parameters match spec (names, types, format)

### 0b. WireMock Mappings Verification

**MUST be obtained before implementation:**

- [ ] WireMock mappings obtained from:
  - Smartsheet SDK tests repo: https://github.com/smartsheet/smartsheet-sdk-tests
  - OR user-provided path on local filesystem
- [ ] **Cannot proceed without mappings - ask user if not provided**
- [ ] Mapping exists for: `/{resource}/{method}/all-response-body-properties`
- [ ] Mapping exists for: `/{resource}/{method}/required-response-body-properties` (if applicable)
- [ ] Global error mappings verified: `/errors/400-response`, `/errors/500-response`
- [ ] Response jsonBody in mappings matches OpenAPI spec schema
- [ ] Request body schema in mappings matches OpenAPI spec (for POST/PUT/PATCH)

### 1. Resource Method Implementation

**File:** `smartsheet/{resource}.py`

**ALL items must match OpenAPI spec exactly:**

- [ ] **Type definitions created** for request/response models (MANDATORY for new endpoints)
- [ ] **Python 3.7 compatibility verified** - type hints, syntax, no 3.8+ features
- [ ] Method signature with proper type hints (parameter types from spec)
- [ ] Parameter names match spec (snake_case conversion from camelCase)
- [ ] Required vs optional parameters match spec
- [ ] Docstring with Args and Returns sections (descriptions from spec)
- [ ] Create operation: `_op = fresh_operation("method_name")`
- [ ] Set HTTP method from spec: `_op["method"] = "GET/POST/PUT/DELETE"`
- [ ] Set path with placeholders from spec: `_op["path"] = "/resource/{id}"`
- [ ] Add query params matching spec: `_op["query_params"]["param"] = value`
- [ ] Add request body matching spec schema (if POST/PUT/PATCH): `_op["json"] = payload`
- [ ] Define expected response type from spec: `expected = "ModelName"` or `["Result", "ModelName"]`
- [ ] Prepare and execute: `prepped = self._base.prepare_request(_op)` then `return self._base.request(prepped, expected, _op)`
- [ ] Return type from spec: `Union[ExpectedType, Error]`
- [ ] **All type definitions use Python 3.7 compatible syntax**

**Reference:** See @ADVANCED.md "Resource Module Organization" for delegation pattern

### 2. Mock API Tests (5 Required Types)

**File:** `tests/mock_api/{resource}/test_{method_name}.py`

**CRITICAL: All 5 test types MUST exist. Tests MUST strictly follow @TESTING.md standards. No exceptions - this is a MANDATORY checklist for development.**

**GOLD STANDARD: Use tests/mock_api/reports/ as your template. Copy the assertion patterns, structure, and style exactly.**

**Test data must match OpenAPI spec:**
- Request parameters use spec-defined types and formats
- Response assertions match spec schema exactly
- Error responses match spec error schemas

- [ ] **`test_{method}_generated_url_is_correct`**
  - Use `uuid.uuid4().hex` for request_id
  - Call `get_mock_api_client(test_scenario_name, request_id)`
  - Execute SDK method
  - Use `get_wiremock_request(request_id)` to retrieve actual request
  - Parse URL with `urlparse()` and `parse_qs()`
  - Assert complete query object: `assert query == {...}` (NOT property-by-property) [TESTING.md lines 73-74]
  - **ALWAYS assert query parameters, even if empty:** `assert not query`
  - Assert URL path matches expected

- [ ] **`test_{method}_all_response_properties`**
  - Call SDK method with test scenario
  - Assert response type with `isinstance(response, ExpectedType)`
  - For wrapped responses (Result, IndexResult): assert BOTH wrapper and inner type
  - Assert complete response: `assert response.to_dict() == {...}` (whole object, NOT properties)
  - **Response structure must match OpenAPI spec schema exactly**
  - Retrieve request with `get_wiremock_request(request_id)`
  - Parse body with `json.loads(wiremock_request["body"])`
  - Assert complete request body: `assert request_body == {...}`
  - **ALWAYS assert request body, even if empty for GET/DELETE:** `assert not request_body`
  - For POST/PUT/PATCH: **Request body must match OpenAPI spec schema (camelCase, correct types)**

- [ ] **`test_{method}_required_response_properties`** (if applicable)
  - Same pattern as all_response_properties
  - Only create if WireMock mapping exists for minimal response
  - Tests SDK handles responses with only required fields
  - **ALWAYS assert request body, even if empty for GET/DELETE:** `assert not request_body`

- [ ] **`test_{method}_error_4xx`**
  - Use test scenario `/errors/400-response` (catch-all)
  - Call SDK method
  - Assert `isinstance(response, Error)`

- [ ] **`test_{method}_error_5xx`**
  - Use test scenario `/errors/500-response` (catch-all)
  - Call SDK method
  - Assert `isinstance(response, Error)`

**Constants file:** `tests/mock_api/{resource}/common_test_constants.py`
- [ ] Add test constants for IDs, expected values, enums

**MANDATORY REFERENCE:** 
- See @TESTING.md "Mock API Test Standards" for complete assertion rules
- **Use tests/mock_api/reports/ as your implementation template - copy the patterns exactly**

### 3. WireMock Mappings

**Repository:** [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests)

**Required mappings:**
- [ ] `{resource}/{method}/all-response-body-properties.json`
- [ ] `{resource}/{method}/required-response-body-properties.json` (if applicable)
- [ ] Error mappings exist globally: `/errors/400-response`, `/errors/500-response`

**Mapping structure (must match OpenAPI spec):**
```json
{
  "request": {
    "urlPathTemplate": "/2.0/{resource}/{id}",
    "method": "GET",
    "headers": {
      "Authorization": {"matches": "Bearer .*"},
      "x-test-name": {"equalTo": "/{resource}/{method}/all-response-body-properties"},
      "x-request-id": {"matches": ".*"}
    }
  },
  "response": {
    "status": 200,
    "jsonBody": { /* Must match OpenAPI response schema */ }
  }
}
```

- [ ] Response jsonBody matches OpenAPI spec response schema exactly
- [ ] Request body schema matches spec (for POST/PUT/PATCH mappings)
- [ ] Status codes match spec

### 4. Documentation Updates

**File:** `docs-source/smartsheet_api.rst` (for API resources)

- [ ] **Check if docs-source update required** (see @ADVANCED.md for when updates are needed)
- [ ] Add method to appropriate module section
- [ ] Follow automodule pattern: `.. automethod:: {ResourceClass}.{method_name}`
- [ ] Rebuild docs: `uv run sphinx-build -b html docs-source docs-source/_build/html`
- [ ] Verify in `docs-source/_build/html/index.html`

**Reference:** See @CONTRIBUTING.md "Documentation" section for file mappings and @ADVANCED.md for documentation requirements

## Quick Reference: SDK Patterns

| Endpoint Type | Request Body | Response Type | Test Count |
|---------------|--------------|---------------|------------|
| GET single | None | `Model` or Error | 5 (skip required if N/A) |
| GET list | None | `IndexResult[Model]` | 5 |
| POST | `_op["json"]` | `Result[Model]` | 5 (must test request body) |
| PUT | `_op["json"]` | `Result[Model]` | 5 (must test request body) |
| DELETE | None | `Result[None]` | 5 |

## Common Mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| "I don't need the spec" | Cannot verify correctness without it | Get spec URL/path first |
| "Spec roughly matches" | SDK must match spec exactly | Verify every parameter/field |
| "Implementation done" | Tests + docs still needed (~80% of work) | Complete all 4 checklist sections |
| "Endpoint is production-ready" | Without tests? No, it's 20% done | All 5 test types required |
| "I'll add tests later" | Tests verify correctness NOW | Tests before marking complete |
| Skipping TodoWrite | Incomplete work looks complete | Create todos FIRST, always |
| Property-by-property assertions | Allows extra properties to creep in | Use `.to_dict() == {...}` |
| Missing request body assertions | Request serialization bugs undetected | Assert `request_body == {...}` for POST/PUT/PATCH |
| Skipping error tests | Error handling untested | Both 4xx and 5xx required |
| Only 3 of 5 test types | Incomplete coverage | All 5 types MUST exist |
| "Docs are obvious" | Sphinx won't auto-discover | Must add to .rst files |
| "Quick implementation" without todos | 80% of work gets skipped | Todos first, no exceptions |
| Tests don't match TESTING.md | Standards exist for a reason | Follow @TESTING.md strictly |
| "I don't need WireMock mappings yet" | Tests will fail without them | Get mappings location first |
| "Mappings can be created later" | Tests depend on mappings existing | Mappings prerequisite, not optional |
| Missing type definitions | Type definitions MANDATORY for new endpoints | Create type defs first |
| Using Python 3.8+ features | Must support 3.7 | Check syntax compatibility |
| Skipping docs check | ADVANCED.md defines requirements | Verify docs needed |

## Red Flags - STOP and Complete Checklist

These thoughts mean STOP - you're taking shortcuts:

- **No OpenAPI spec verified** - Cannot proceed without spec
- **No WireMock mappings verified** - Cannot proceed without mappings
- **Haven't reviewed reports tests** - Must review gold standard template first
- "I'll check the spec later" - Spec MUST be verified first
- "I know the pattern" - Review reports tests anyway, don't rely on memory
- "Mappings probably exist" - Must verify, not assume
- Only implementation file changed (no tests/docs)
- "Implementation complete" or "endpoint is production-ready"
- "Quick implementation" without TodoWrite
- No todos created from checklist
- Missing any of 5 test types
- WireMock mappings not created
- Tests use property-by-property assertions
- Documentation not updated
- "I'll add tests/docs in follow-up PR"
- "Tests can wait" or "just need implementation"
- Started coding before creating todos
- Request/response doesn't match spec exactly
- No type definitions created for new endpoint
- Using Python 3.8+ syntax (walrus operator, positional-only params)
- Didn't check ADVANCED.md for docs requirements

**All of these mean: Work incomplete. Return to checklist, verify spec and mappings, create ALL todos first.**

**Implementation without spec verification, mappings, tests, and docs is NOT production-ready. It's 20% done.**

## Example: Complete Implementation

**NOTE: This is a simplified example. For complete gold standard implementation, see tests/mock_api/reports/test_create_report.py**

**Scenario:** Add `Contacts.get_contact(contact_id)`

### 1. Resource Method
```python
# smartsheet/contacts.py
def get_contact(self, contact_id: str) -> Union[Contact, Error]:
    """Get a contact by ID.
    
    Args:
        contact_id (str): Contact ID (email address)
    
    Returns:
        Union[Contact, Error]: Contact object or Error
    """
    _op = fresh_operation("get_contact")
    _op["method"] = "GET"
    _op["path"] = f"/contacts/{contact_id}"
    
    expected = "Contact"
    prepped = self._base.prepare_request(_op)
    return self._base.request(prepped, expected, _op)
```

### 2. Tests (5 types)
```python
# tests/mock_api/contacts/test_get_contact.py
import uuid
from urllib.parse import urlparse
from smartsheet.models import Contact, Error
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client, get_wiremock_request
)

def test_get_contact_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/contacts/get-contact/all-response-body-properties", request_id
    )
    
    client.Contacts.get_contact("user@example.com")
    
    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == "/2.0/contacts/user@example.com"

def test_get_contact_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/contacts/get-contact/all-response-body-properties", request_id
    )
    
    response = client.Contacts.get_contact("user@example.com")
    
    assert isinstance(response, Contact)
    assert response.to_dict() == {
        "id": "user@example.com",
        "email": "user@example.com",
        "name": "User Name"
    }

def test_get_contact_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/400-response", request_id)
    
    response = client.Contacts.get_contact("invalid")
    assert isinstance(response, Error)

def test_get_contact_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/500-response", request_id)
    
    response = client.Contacts.get_contact("user@example.com")
    assert isinstance(response, Error)
```

### 3. Documentation
```rst
# docs-source/smartsheet_api.rst
Contacts
--------
.. automethod:: Contacts.get_contact
```

## The Bottom Line

**Implementation without tests and documentation is incomplete work.**

The baseline pattern: agents write implementation quickly, then stop at ~20% complete. Time pressure triggers "implementation = done" rationalization.

Follow the 4-part checklist completely. All 5 test types are required. Whole-object assertions prevent regressions. Documentation updates are not optional.

**No Exceptions:**
- Not for "simple endpoints" - all require tests
- Not for "modifications" - updated endpoints need updated tests
- Not for "time pressure" - incomplete work creates more pressure later
- Not for "stakeholder waiting" - shipping untested code is worse
- Never skip TodoWrite - creates accountability

**The rule: Create ALL todos from checklist FIRST. Then complete them. Mark done only when all 4 components exist.**
