# Testing Guide

This guide establishes the mandatory patterns for mock API testing in the Smartsheet Python SDK.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running Mock API Tests](#running-mock-api-tests)
- [Mock API Test Standards](#mock-api-test-standards)
  - [Standardized Test Cases](#standardized-test-cases)
  - [Key Principles](#key-principles)
  - [Test Suite Structure](#test-suite-structure)
- [Additional Rules](#additional-rules)
- [Helper Functions](#helper-functions)

---

## Getting Started

### Prerequisites

Mock API tests require WireMock running locally on port 8082. The WireMock server provides simulated API responses for contract testing without hitting the live Smartsheet API.

For WireMock setup instructions, mapping documentation, and details on `x-request-id` and `x-test-name` header usage, see the [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests) repository.

For complete test examples, see [tests/mock_api/reports/](tests/mock_api/reports/).

### Running Mock API Tests

| Command | Purpose |
| ------- | ------- |
| `uv run pytest tests/mock_api` | Run all mock API tests |
| `uv run pytest tests/mock_api/reports/test_create_report.py` | Run specific test suite |
| `uv run pytest tests/mock_api/reports/test_create_report.py::test_create_report_all_response_properties -v` | Run specific test |

---

## Mock API Test Standards

### Standardized Test Cases

Every endpoint must implement these test cases (using snake_case naming for Python):

**Required Tests:**

1. **`<method>_generated_url_is_correct`**
   - Asserts request method
   - Asserts URL path
   - Asserts query parameters (even if empty: `assert not query`)
   - Does NOT assert request/response body

2. **`<method>_all_response_properties`**
   - Asserts request body (even if empty for GET/DELETE: `assert not request_body`)
   - Asserts response body with all properties
   - Does NOT assert method, URL, or query parameters

3. **`<method>_error_4xx`**
   - Asserts ONLY that SDK returns expected client error (using `isinstance(response, Error)`)

4. **`<method>_error_5xx`**
   - Asserts ONLY that SDK returns expected server error (using `isinstance(response, Error)`)

**Optional Tests:**

- **`<method>_required_response_properties`** - Include ONLY if a corresponding WireMock mapping exists for the required-properties variant. Asserts minimal request (even if empty for GET/DELETE: `assert not request_body`) and response body.
- **Endpoint-specific tests** - Additional tests for unique endpoint behaviors (e.g., scope variants, role differences, state variations)

### Key Principles

#### Full-Object Assertions

Assert objects as a whole using `==` comparison, not property-by-property. This ensures extra or missing properties cause test failures.

- **Query parameters:** Assert the entire query parameter dict after parsing with `parse_qs()`
- **Request body:** Assert the entire request body dict
- **Response body:** Assert the entire deserialized response object using `.to_dict()`

#### Test Constants

- **Cross-file constants:** Use reusable constants from `common_test_constants.py` (e.g., `TEST_REPORT_ID`, `TEST_SHEET_ID`)
- **File-scoped constants:** Define expected responses, request bodies, and query params at the top of each test file

#### WireMock Integration

Each test uses custom headers for WireMock integration:

- **`x-request-id`:** UUID for request tracking (retrieve via `get_wiremock_request()`)
- **`x-test-name`:** Targets specific WireMock mapping (e.g., `/reports/create-report/all-response-body-properties`)

See [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests) for WireMock mapping conventions and header usage details.

### Test Suite Structure

- **One test file per endpoint:** `tests/mock_api/<resource>/test_<endpoint_name>.py`
- **One constants file per resource:** `tests/mock_api/<resource>/common_test_constants.py`
- **Gold standard examples:** See `tests/mock_api/reports/` for complete test implementations

---

## Additional Rules

- **isinstance validation:** Use `isinstance()` for response body validation on both wrapper (e.g., `Result`) and inner object (e.g., `CreateReportResult`)
- **Enum usage:** Use enums when constructing request body and query params (e.g., `ReportDestinationType.FOLDER`)
- **Assertion format:** Use raw dicts with `response.to_dict()` when asserting request/response bodies and query parameters

---

## Helper Functions

**Available in `tests/mock_api/mock_api_test_helper.py`:**

- **`get_mock_api_client(test_name, request_id)`** - Creates a Smartsheet client configured for WireMock server (<http://localhost:8082/2.0/>)
- **`get_wiremock_request(request_id)`** - Retrieves request from WireMock admin API using the `x-request-id` header. Returns request object with `absoluteUrl`, `body`, `headers`, `method`, etc.
