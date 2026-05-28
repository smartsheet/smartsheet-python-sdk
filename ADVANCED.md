# Advanced Topics for the Smartsheet SDK for Python

## Table of Contents

- [SDK Architecture](#sdk-architecture)
  - [Client Initialization](#client-initialization)
  - [Request Lifecycle](#request-lifecycle)
  - [Response Handling](#response-handling)
  - [Error Handling and Exceptions](#error-handling-and-exceptions)
  - [Retry Logic and Backoff](#retry-logic-and-backoff)
  - [Serialization and Deserialization](#serialization-and-deserialization)
  - [Pagination Handling](#pagination-handling)
  - [Model Object Construction](#model-object-construction)
  - [Resource Module Organization](#resource-module-organization)
  - [Passthrough Internals](#passthrough-internals)
  - [Logging Infrastructure](#logging-infrastructure)
  - [Authentication Flow](#authentication-flow)
- [Manual Install](#manual-install)
- [Logging](#logging)
- [Passthrough Option](#passthrough-option)
- [Testing](#testing)
- [HTTP Proxy](#http-proxy)
- [Event Reporting](#event-reporting)
- [Working with Smartsheetgov.com Accounts](#working-with-smartsheetgovcom-accounts)
- [Working With Smartsheet Regions Europe Accounts](#working-with-smartsheet-regions-europe-accounts)

## SDK Architecture

This section provides detailed insight into the internal architecture of the Smartsheet Python SDK, covering the core subsystems that power API interactions. Understanding these patterns enables advanced customization, troubleshooting, and integration work.

### Client Initialization

The SDK entry point begins with the `Smartsheet` class constructor (`smartsheet/smartsheet.py:147-218`), which orchestrates several initialization steps. Token resolution follows a priority order: constructor parameter first, then `SMARTSHEET_ACCESS_TOKEN` environment variable, raising `ValueError` if neither is provided. The client configures a backoff calculator (`smartsheet/smartsheet.py:188-191`), accepting either an integer for `DefaultCalcBackoff` or a custom `AbstractUserCalcBackoff` instance to control retry timing. An HTTP session with connection pooling is created via `pinned_session()` (`smartsheet/session.py:51-64`), defaulting to 8 connections with SSL pinning that disables SSLv2, SSLv3, and TLSv1. The user agent string is built as `SmartsheetPythonSDK/{version}/{caller}`, auto-detecting the caller module from the call stack or accepting a custom string (`smartsheet/smartsheet.py:197-206`). Finally, logging is configured via `setup_logging()` which respects the `LOG_CFG` environment variable for custom log levels or JSON configuration files. Resource modules like `Sheets` and `Users` are lazy-loaded on first access through `__getattr__` (`smartsheet/smartsheet.py:499-531`), caching instances in `_api_modules_cache` to avoid repeated imports. The SDK supports three base URLs: US (`https://api.smartsheet.com/2.0`), EU (`https://api.smartsheet.eu/2.0`), and Government (`https://api.smartsheetgov.com/2.0`), selectable via the `api_base` constructor parameter.

**Cross-reference:** See [Authentication Flow](#authentication-flow) for token handling details, [Retry Logic and Backoff](#retry-logic-and-backoff) for backoff configuration, and [Resource Module Organization](#resource-module-organization) for lazy loading patterns.

### Request Lifecycle

API requests flow through a delegation pattern where resource methods construct operation dictionaries, delegate to `prepare_request()`, and execute via `request()`. Resource methods (`smartsheet/sheets.py` and similar) use `fresh_operation()` to create a standardized operation dictionary containing keys like `method`, `path`, `json`, `query_params`, and `header_params`. For example, adding rows constructs an operation with `method="POST"`, `path="/sheets/{id}/rows"`, and `json=list_of_rows`. The `prepare_request()` method (`smartsheet/smartsheet.py:429-497`) transforms this operation by merging header parameters, substituting path placeholders like `{key}` with actual values, serializing JSON bodies via `serialize()`, and converting list query parameters to comma-separated strings. It creates a `requests.Request` object and calls `session.prepare_request()` to produce a `PreparedRequest` with URL encoding and proper formatting. Standard headers are then injected: User-Agent, Authorization (Bearer token), and optional headers like Assume-User for impersonation, Api-Scenario for test scenarios, and Smartsheet-Change-Agent for audit tracking. The prepared request is passed to `request()` which executes it with retry logic and returns a deserialized response. This pattern ensures consistent authentication, serialization, and error handling across all API operations.

**Cross-reference:** See [Serialization and Deserialization](#serialization-and-deserialization) for JSON body handling, [Authentication Flow](#authentication-flow) for header injection, and [Retry Logic and Backoff](#retry-logic-and-backoff) for request execution with retries.

```text
┌──────────────────┐
│ Resource Method  │  e.g., sheets.add_rows()
└────────┬─────────┘
         │ Creates operation dict
         ▼
┌──────────────────┐
│ prepare_request  │  Serializes JSON, injects headers
└────────┬─────────┘
         │ Returns PreparedRequest
         ▼
┌──────────────────┐
│ request_with_retry│ Executes HTTP request with retry logic
└────────┬─────────┘
         │ Returns OperationResult or OperationErrorResult
         ▼
┌──────────────────┐
│ native()         │  Deserializes to model objects
└──────────────────┘
```

### Response Handling

Response handling branches based on HTTP status codes to return either success or error results. The `_request()` method (`smartsheet/smartsheet.py:359-385`) returns `OperationResult` for 2xx status codes or `OperationErrorResult` for all other codes. The `OperationResult` class (`smartsheet/smartsheet.py:534-623`) stores the JSON response text, raw `requests.Response` object, base client reference, and operation metadata. Its `native()` method performs type-based model instantiation by dynamically importing model classes from `smartsheet.models` based on the `expected` parameter. For standard types like `"Sheet"` or `"User"`, it imports the class and instantiates it with the parsed JSON data. For list types specified as `["IndexResult", "Contact"]`, it instantiates the container class with a dynamic type parameter to handle polymorphic data collections. Special handling exists for `DownloadedFile` responses, which extract filenames from Content-Disposition headers and return metadata without deserializing binary content. Model objects receive the raw HTTP response via the `request_response` attribute, enabling access to headers and status codes. The `request()` method (`smartsheet/smartsheet.py:280-308`) calls `result.native(expected)` to convert the result, then optionally raises exceptions based on the `raise_exceptions` flag. Dynamic imports enable flexible type handling and avoid loading unused model classes, while response attachment preserves metadata for debugging.

**Cross-reference:** See [Model Object Construction](#model-object-construction) for deserialization details, [Error Handling and Exceptions](#error-handling-and-exceptions) for error responses, and [Pagination Handling](#pagination-handling) for paginated result types.

### Error Handling and Exceptions

The SDK implements dual-mode error handling: result mode (default) returns `Error` model instances, while exception mode raises typed exceptions. The error hierarchy begins with `SmartsheetException` as the base, extending to `ApiError` (errorCode 0, no retry), `HttpError` (HTTP layer failures), `InternalServerError` (5xx errors), and retryable errors like `SystemMaintenanceError` (4001), `ServerTimeoutExceededError` (4002), `RateLimitExceededError` (4003), and `UnexpectedErrorShouldRetryError` (4004). The `error_lookup` dictionary (`smartsheet/smartsheet.py:628-662`) maps error codes to exception metadata including class name, retry recommendation, and `should_retry` boolean flag. When a non-2xx response is received, `OperationErrorResult.native()` parses the JSON error code and constructs an `Error` model with an `ErrorResult` containing code, message, exception name, recommendation, and retry flag. If `raise_exceptions=True` (configured via `errors_as_exceptions(True)`), the `request()` method dynamically imports the exception class by name and raises it with the Error object and formatted message. Otherwise, the Error model is returned for application-level handling. This dual approach provides flexibility for different error handling strategies while preserving complete error metadata including correlation IDs for support requests.

**Cross-reference:** See [Retry Logic and Backoff](#retry-logic-and-backoff) for retry-eligible error codes and [Response Handling](#response-handling) for error result construction.

**Implementation locations:**

- Exception definitions: `smartsheet/exceptions.py:20-131`
- Error lookup and raising: `smartsheet/smartsheet.py:625-721, 299-308`
- Configuration method: `smartsheet/smartsheet.py:235-248`
- Error models: `smartsheet/models/error.py`, `smartsheet/models/error_result.py`

### Retry Logic and Backoff

Retry logic applies exclusively to retryable errors identified by the `should_retry` flag in the error_lookup dictionary. The `request_with_retry()` method (`smartsheet/smartsheet.py:387-427`) wraps `_request()` in a loop that checks each `OperationErrorResult` for `should_retry=True`. Retryable error codes include 4001 (SystemMaintenanceError), 4002 (ServerTimeoutExceededError), 4003 (RateLimitExceededError), and 4004 (UnexpectedErrorShouldRetryError), while non-retryable errors immediately break the loop. The backoff strategy uses `DefaultCalcBackoff` (`smartsheet/smartsheet.py:93-116`), which implements exponential backoff with jitter: `(2^attempt) + random.random()`, producing delays of 1-2s, 4-5s, 8-9s, etc. The calculator checks elapsed time against `max_retry_time` (default 30 seconds) and returns -1 when exceeded to terminate retries. Custom backoff behavior is supported by implementing `AbstractUserCalcBackoff` and passing it to the constructor. Before each retry, the request's authorization token is restored (it was redacted during logging) and the attempt counter increments. Retry attempts are logged at INFO level with the calculated backoff duration. This approach balances automatic recovery from transient failures with preventing infinite retry loops, while the extensible calculator interface enables custom strategies for specific deployment scenarios.

**Cross-reference:** See [Error Handling and Exceptions](#error-handling-and-exceptions) for retryable error codes, [Request Lifecycle](#request-lifecycle) for the retry loop context, and [Logging Infrastructure](#logging-infrastructure) for retry logging.

**Backoff formula flow:**

```text
Attempt 0: 2^0 + random(0,1) = 1-2s
Attempt 1: 2^1 + random(0,1) = 2-3s
Attempt 2: 2^2 + random(0,1) = 4-5s
Attempt 3: 2^3 + random(0,1) = 8-9s
```

### Serialization and Deserialization

The SDK uses bidirectional type conversion between Python objects and JSON through `serialize()` and `deserialize()` functions. Serialization (`smartsheet/util.py:105-162`) recursively processes objects with priority-based handling: custom `.serialize()` methods, datetime to ISO 8601 with "Z" suffix, date to ISO 8601 date-only, primitives (str, int, float, bool) as-is, `EnumeratedValue` to enum name string, lists to recursively serialized arrays (returning None for empty lists), and dicts to recursively serialized objects with camelCase key conversion. The `None` value handling is nuanced: None in object properties is skipped, None in dict values is preserved, and `ExplicitNull` objects are excluded entirely. Type wrapper classes in `smartsheet/types.py` enforce type safety: `String` (with optional accept whitelist), `Number` (int/float), `Boolean` (strict bool), `Timestamp` (datetime or ISO string with auto-parsing via dateutil), `EnumeratedValue` (string or Enum with flexible lookup by name or value), `TypedList` (homogeneous collections with automatic item conversion), and `TypedObject` (nested models with dict-to-instance conversion). Deserialization (`smartsheet/util.py:165-174`) iterates dict items, converts camelCase keys to snake_case via regex, and calls `setattr()` which triggers type wrapper validation. Property introspection (`get_child_properties()`) discovers all `@property` decorated methods and generates (snake_case, camelCase) tuples for serialization. Model classes implement `to_dict()` (calls serialize) and `to_json()` (calls json.dumps on dict) for request payloads. This type system provides automatic coercion, validation, and naming convention translation while supporting recursive nested structures and polymorphic collections.

**Cross-reference:** See [Model Object Construction](#model-object-construction) for deserialization in model **init**, [Request Lifecycle](#request-lifecycle) for serialization in prepare_request, and [Response Handling](#response-handling) for native() deserialization.

**Name convention mapping:**

- `destinationId` ↔ `destination_id`
- `createdAt` ↔ `created_at`
- `modifiedBy` ↔ `modified_by`

### Pagination Handling

The SDK supports three pagination patterns through specialized result wrapper classes. `IndexResult` (`smartsheet/models/index_result.py`) implements offset-based pagination with properties `page_number`, `page_size`, `total_count`, `total_pages`, and optionally `last_key` for optimization. API consumers send `pageSize` and `page` query parameters or `includeAll=true` to bypass pagination. This pattern suits browseable datasets where total count is needed. `TokenPaginatedResult` (`smartsheet/models/token_paginated_result.py`) implements cursor-based pagination with `data` and `last_key` properties. Consumers pass `maxItems` and `lastKey` query parameters, iterating until `last_key` is None. This pattern is efficient for large datasets and real-time feeds where total count is unavailable. `EventResult` (`smartsheet/models/event_result.py`) implements stream-position pagination for event streams, with `data`, `more_available`, and `next_stream_position` properties. The initial request uses `since` (UNIX ms or ISO-8601 timestamp), subsequent requests use `streamPosition`, and iteration continues while `more_available=True`. All pagination classes use `Generic[T]` for type safety and accept a `dynamic_data_type` parameter during instantiation. The response flow through `OperationResult.native()` uses list-based expected parameters like `["IndexResult", "Contact"]` to dynamically instantiate the wrapper with the correct item type. Deserialization automatically maps JSON keys (`pageNumber`, `moreAvailable`, etc.) to Python properties (`page_number`, `more_available`) via camelCase-to-snake_case conversion. Raw HTTP responses are accessible via `request_response` for accessing headers and debugging.

**Cross-reference:** See [Response Handling](#response-handling) for dynamic type instantiation, [Serialization and Deserialization](#serialization-and-deserialization) for naming convention conversion, and [Model Object Construction](#model-object-construction) for Generic type handling.

**Pagination comparison:**

| Pattern | IndexResult | TokenPaginatedResult | EventResult |
| ------- | ----------- | -------------------- | ----------- |
| Type | Offset-based | Cursor-based | Stream position |
| Total count | Yes | No | No |
| Use case | Small datasets | Large datasets | Event streams |
| Parameters | page, pageSize | lastKey, maxItems | streamPosition, since |

### Model Object Construction

Model construction follows a declarative builder pattern where classes initialize typed attribute wrappers and deserialize JSON dictionaries. All model `__init__` methods (`smartsheet/models/*.py`) accept optional `props` (JSON dict) and `base_obj` (Smartsheet client reference) parameters. Construction proceeds in four steps: store base_obj reference, initialize typed attributes (e.g., `self._id_ = Number()`, `self._name = String()`, `self._rows = TypedList(Row)`), call `deserialize(self, props)` to populate attributes from JSON, and mark initialization complete. The deserialize function converts camelCase JSON keys to snake_case Python attributes via regex and calls `setattr()`, which triggers property setters that delegate to type wrapper `.value` setters. Type coercion happens automatically: String validates string types, Number accepts int/float, Boolean accepts bool only, Timestamp accepts datetime or ISO string (parsing via dateutil), EnumeratedValue accepts string or Enum (trying name then value lookup), TypedList converts items to the specified type recursively, and TypedObject converts dicts to nested model instances. Nested object composition uses TypedObject for single optional references (e.g., `created_by: User`) and TypedList for homogeneous arrays (e.g., `rows: List[Row]`). Circular import issues are handled with deferred imports inside `__init__`. The reverse serialization process uses `to_dict()` (calls `serialize(self)`) and `to_json()` (calls `json.dumps(to_dict())`) to convert models back to JSON for API requests, with automatic camelCase conversion and None filtering. Type string references enable lazy loading: `TypedList("Row")` imports the Row class on first use, avoiding circular dependencies at class definition time.

**Cross-reference:** See [Serialization and Deserialization](#serialization-and-deserialization) for type system details, [Response Handling](#response-handling) for model instantiation from API responses, and [Request Lifecycle](#request-lifecycle) for serialization back to JSON.

**Construction flow:**

```python
# API response: {"id": 123, "name": "Sheet", "rows": [{"id": 1}]}
sheet = Sheet(api_response, base_obj=client)

# Internally:
# 1. self._id_ = Number()
# 2. self._name = String()
# 3. self._rows = TypedList(Row)
# 4. deserialize: "id" → self.id_ = 123 → Number().value = 123
# 5. deserialize: "name" → self.name = "Sheet" → String().value = "Sheet"
# 6. deserialize: "rows" → self.rows = [...] → TypedList converts dicts to Row instances
```

### Resource Module Organization

Resource modules organize API operations through classes that delegate to the base Smartsheet client. Each resource class (`smartsheet/sheets.py`, `smartsheet/users.py`, etc.) follows a consistent structure: accept `smartsheet_obj` in `__init__`, store as `self._base`, create a logger as `self._log`, and implement operation methods with standard naming conventions. Method prefixes indicate operation types: `list_*` for retrieving multiple resources, `get_*` for retrieving single resources by ID, `add_*` for creating resources, `update_*` for modifying resources, `delete_*` for removing resources, and custom actions like `publish_*` or `promote_*`. Each method creates an operation dictionary via `fresh_operation()`, sets `method`, `path`, `json`, and `query_params`, defines `expected` response types (e.g., `["Result", "Column"]`), calls `self._base.prepare_request(_op)`, calls `self._base.request(prepped_request, expected, _op)`, and returns the result. This delegation pattern separates operation definition from HTTP execution, ensuring consistent authentication, error handling, and serialization across all endpoints. Resource modules are lazy-loaded via `Smartsheet.__getattr__` (`smartsheet/smartsheet.py:499-531`): first access dynamically imports the module (e.g., `smartsheet.sheets`), instantiates the class with the client as parameter, caches the instance in `_api_modules_cache`, and returns the cached instance on subsequent accesses. This approach provides on-demand loading for memory efficiency and a clean attribute-based API (`client.sheets.list_sheets()`).

**Cross-reference:** See [Client Initialization](#client-initialization) for lazy loading details, [Request Lifecycle](#request-lifecycle) for operation dictionary processing, and [Error Handling and Exceptions](#error-handling-and-exceptions) for return type Union handling.

**Operation method pattern:**

```python
def add_columns(self, sheet_id, list_of_columns):
    _op = fresh_operation("add_columns")
    _op["method"] = "POST"
    _op["path"] = f"/sheets/{sheet_id}/columns"
    _op["json"] = list_of_columns
    expected = ["Result", "Column"]
    prepped = self._base.prepare_request(_op)
    return self._base.request(prepped, expected, _op)
```

### Passthrough Internals

The Passthrough class (`smartsheet/passthrough.py`) provides raw JSON-level API access for endpoints without typed SDK methods. It implements four methods mirroring HTTP verbs: `get(endpoint, query_params)`, `post(endpoint, payload, query_params)`, `put(endpoint, payload, query_params)`, and `delete(endpoint)`. Each method creates an operation dictionary via `fresh_operation()`, sets the HTTP method and endpoint path, wraps payloads in `JSONObject` if needed (accepts dict, JSON string, or JSONObject), calls `self._base.prepare_request(_op)`, calls `self._base.request(prepped_request, "JSONObject", _op)`, and returns `JSONObject` or `Error`. The `JSONObject` class is a lightweight wrapper that stores raw JSON data in `_data`, accepts dict or JSON string in `__init__`, and provides `serialize()` and `to_dict()` methods that return the inner dict unchanged, bypassing the SDK's type system entirely. This enables accessing newly released API features, experimental endpoints, and arbitrary request construction without type constraints. Passthrough limitations include no type safety (typos caught only after API round-trip), no automatic serialization (dates, enums, camelCase conversion handled manually by developer), no return type information (generic JSONObject wrapper), no pagination helpers, API URL construction errors caught only at runtime, limited query parameter support (DELETE doesn't accept query params), and no response validation beyond Error detection. The migration path is straightforward: passthrough usage signals missing SDK features, maintainers add typed methods based on usage patterns, and applications gain type safety by replacing passthrough calls with typed methods.

**Cross-reference:** See [Serialization and Deserialization](#serialization-and-deserialization) for how passthrough bypasses type conversion, [Request Lifecycle](#request-lifecycle) for shared operation processing, and [Resource Module Organization](#resource-module-organization) for comparison with typed methods.

**Passthrough vs Typed Methods:**

| Aspect | Typed Methods | Passthrough |
| ------ | ------------- | ----------- |
| Input | Model objects | Dict/JSON/JSONObject |
| Validation | Type-checked | API-only |
| Serialization | Recursive with conversions | Direct pass-through |
| Property names | Auto camel-cased | Developer responsible |
| Return type | Typed object | JSONObject wrapper |

### Logging Infrastructure

Logging configuration occurs during client initialization via `setup_logging()` (`smartsheet/smartsheet.py:66-84`), which checks the `LOG_CFG` environment variable for three scenarios: unset (uses Python default), file path (loads JSON config via `logging.config.dictConfig()`), or string value ("DEBUG" or "INFO" sets level). Dependency logging is always throttled by setting `requests` and `urllib3` loggers to WARNING level to reduce noise. Request logging happens in `_log_request()` (`smartsheet/smartsheet.py:310-357`), which is called after every HTTP request. INFO level logs contain structured request metadata: `{"request": {"command": "METHOD URL"}}` with minimal overhead. DEBUG level logs include request body (JSON parsed and formatted with sorted keys, multipart suppressed, other content types suppressed) and successful response body (JSON parsed/formatted for normal responses, body omitted for downloads via dl_path check). ERROR level logs contain failed response details: `{"response": {"statusCode": code, "reason": text, "content": body}}` with JSON parsing for JSON responses. Performance implications vary by level: INFO has negligible overhead (simple string concatenation), DEBUG has moderate overhead (JSON parsing and sorting on every request/response), and ERROR has low frequency impact (only on failures). Optimizations include conditional JSON parsing (only if Content-Type is application/json), multipart detection (skips body logging for multipart requests via is_multipart() utility), download path optimization (skips response body logging when operation[dl_path] is set to save memory on binary downloads), and dependency throttling (reduces framework noise). Retry attempts log at INFO level with backoff duration. Security considerations include full request/response body logging (may contain sensitive data) and multipart body suppression (prevents logging files).

**Cross-reference:** See [Client Initialization](#client-initialization) for setup_logging() integration, [Request Lifecycle](#request-lifecycle) for when `_log_request()` is called, and [Retry Logic and Backoff](#retry-logic-and-backoff) for retry attempt logging.

**Log level content:**

- **INFO**: Request method + URL only
- **DEBUG**: Request body, response body (JSON formatted with sorted keys)
- **ERROR**: Failed response with status code, reason, body

### Authentication Flow

Authentication uses bearer token authentication with no automatic refresh. Token resolution (`smartsheet/smartsheet.py:176-186`) follows a priority order: constructor parameter (highest priority), `SMARTSHEET_ACCESS_TOKEN` environment variable, or ValueError if neither is provided. This fail-fast approach ensures explicit configuration at initialization time. Bearer token header injection occurs in `prepare_request()` (`smartsheet/smartsheet.py:463-466`) only when `auth_settings` is configured for the operation, concatenating "Bearer " + token and updating the Authorization header. The SDK assumes long-lived access tokens and does not implement automatic refresh logic or 401 retry mechanisms, making the application responsible for token rotation and renewal. Special headers support specific use cases: Assume-User header (`smartsheet/smartsheet.py:468-474`) enables admin impersonation via `assume_user(email)`, Api-Scenario header (`smartsheet/smartsheet.py:476-482`) enables test scenario identification via `set_test_scenario(name)`, Smartsheet-Change-Agent header (`smartsheet/smartsheet.py:487-495`) enables audit trail tracking via `set_change_agent(agent)`, and WireMock testing headers (`smartsheet/smartsheet.py:483-485`) include X-Test-Name and X-Request-ID when configured. All special headers follow a cleanup pattern: set when configured, explicitly deleted if not set (via try/except KeyError to handle missing headers gracefully), preventing header pollution across multiple requests. Security considerations include token storage (parameter or environment, never in config files), token transmission over HTTPS with SSL pinning (`smartsheet/session.py`), no caching beyond session lifetime, and authorization header redaction in debug logs.

**Cross-reference:** See [Client Initialization](#client-initialization) for token resolution during construction, [Request Lifecycle](#request-lifecycle) for header injection timing, and [Logging Infrastructure](#logging-infrastructure) for token redaction in logs.

**Authentication architecture:**

```text
Smartsheet.__init__()
  ├─ Token Resolution (parameter > env > ValueError)
  └─ prepare_request()
     ├─ Authorization: Bearer <token>
     ├─ Assume-User (optional impersonation)
     ├─ Api-Scenario (optional test scenario)
     ├─ Smartsheet-Change-Agent (optional audit)
     └─ X-Test-Name/X-Request-ID (optional WireMock)
```

## Manual install

### For End Users

To install the SDK without uv (standard pip installation):

```bash
pip install smartsheet-python-sdk
```

### For Contributors

Contributors should use uv for development. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.

The following packages are the core runtime dependencies:

- [six](https://pypi.python.org/pypi/six)
- [requests](https://pypi.python.org/pypi/requests)
- [requests-toolbelt](https://pypi.org/project/requests-toolbelt/)
- [certifi](https://pypi.org/project/certifi/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)

If you want to install from source without uv:

1. Clone the repo from [GitHub](https://github.com/smartsheet/smartsheet-python-sdk)
2. Ensure you are in the `smartsheet-python-sdk` directory
3. Install it:

   ```bash
   pip install -e .
   ```

## Logging

There are three log levels currently supported by the Smartsheet Python SDK (in increasing order of verbosity):

**ERROR** - messages related to API or JSON serialization errors

**INFO** - messages about the API resources being requested

**DEBUG** - API request and response bodies and messages regarding object attributes that are changed by the SDK due to the nature of the API call being made

Use the logging facility's [basicConfig](https://docs.python.org/2/library/logging.html#logging.basicConfig) method to set your logging properties:

```python
    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
```

## Passthrough Option

If there is an API feature that is not yet supported by the Python SDK, there is a passthrough option that allows you to pass and receive raw JSON objects.

To invoke the passthrough, your code can call one of the following four methods:

`response = client.Passthrough.get(endpoint, query_params)`

`response = client.Passthrough.post(endpoint, payload, query_params)`

`response = client.Passthrough.put(endpoint, payload, query_parameters)`

`response = client.Passthrough.delete(endpoint)`

- `endpoint`: The specific API endpoint you wish to invoke. The client object base URL gets prepended to the caller’s endpoint URL argument, so in the above `get` example, if endpoint is `'/sheets'` an HTTP GET is requested from the URL `https://api.smartsheet.com/2.0/sheets`
- `payload`: The data to be passed through, can be either a dictionary or string.
- `query_params`: An optional dictionary of query parameters.

All calls to passthrough methods return a JSON result. The `data` attribute contains the JSON result as a dictionary. For example, after a PUT operation the API's result message will be contained in `response.data['message']`. If you prefer raw JSON instead of a dictionary, you can use the `to_json()` method, for example `response.to_json()`.

### Passthrough Example

The following example shows how to POST data to `https://api.smartsheet.com/2.0/sheets` using the passthrough method and a dictionary:

```python
payload = {"name": "my new sheet",
            "columns": [
              {"title": "Favorite", "type": "CHECKBOX", "symbol": "STAR"},
              {"title": "Primary Column", "primary": True, "type": "TEXT_NUMBER"}
            ]
          }

response = client.Passthrough.post('/sheets', payload)
```

## Testing

For comprehensive testing documentation, including mock API test standards and examples, see [TESTING.md](TESTING.md).

## HTTP Proxy

The following example shows how to enable a proxy by providing a `proxies` argument when initializing the Smartsheet
client.

```python
# Initialize client
proxies = {
    'https': 'http://127.0.0.1:8888'
}

smartsheet_client = smartsheet.Smartsheet(proxies=proxies)
```

## Event Reporting

The following sample demonstrates best practices for consuming the event stream from the Smartsheet Event Reporting
feature.

The sample uses the `smartsheet_client.Events.list_events` method to request a list of events from the stream. The first
request sets the `since` parameter with the point in time (i.e. event occurrence datetime) in the stream from which to
start consuming events. The `since` parameter can be set with a datetime value that is either formatted as ISO 8601
(e.g. 2010-01-01T00:00:00Z) or as UNIX epoch (in which case the `numeric_dates` parameter must also be set to `True`.
By default the `numeric_dates` parameter is set to `False`).

The sample utilizes the `smartsheet_client.Events.list_events` method to request a list of events up to a certain
point in the stream. The `to` parameter specifies the endpoint in time (i.e., event occurrence datetime) in the stream
up to which events should be retrieved. This `to` parameter can be assigned a datetime value formatted either as
ISO 8601 (e.g., 2020-12-31T23:59:59Z) or as UNIX epoch time, in which case the numeric_dates parameter must be set to True.
If not specified, the `numeric_dates` parameter defaults to `False`, assuming the datetime is in ISO 8601 format.
This allows for precise control over the range of events to be fetched, facilitating efficient data retrieval and processing.

To consume the next list of events after the initial list of events is returned, set the `stream_position` parameter
with the `next_stream_position` property obtained from the previous request and don't set the `since` parameter with
any values. This is because when using the `list_events` method, either the `since` parameter or the `stream_position`
parameter should be set, but never both.

Note that the `more_available` property in a response indicates whether more events are immediately available for
consumption. If events are not immediately available, they may still be generating so subsequent requests should keep
using the same `stream_position` value until the next list of events is retrieved.

Many events have additional information available as a part of the event. That information can be accessed using
the Python dictionary stored in the `additional_details` property (Note that values of the `additional_details`
dictionary use camelCase/JSON names, e.g. `sheetName` not `sheet_name`). Information about the additional details

provided can be found on the [Events Description](https://smartsheet.redoc.ly/tag/eventsDescription) page of the API Documentation.

```python
# this example is looking specifically for new sheet events
def print_new_sheet_events_in_list(events_list):
    # enumerate all events in the list of returned events
    for event in events_list.data:
        # find all created sheets
        if event.object_type == smartsheet.models.enums.EventObjectType.SHEET and event.action == smartsheet.models.enums.EventAction.CREATE:
            # additional details are available for some events, they can be accessed as a Python dictionary
            # in the additional_details attribute
            print(event.additional_details['sheetName'])


smartsheet_client = smartsheet.Smartsheet()
smartsheet_client.errors_as_exceptions()

# begin listing events in the stream starting with the `since` parameter
last_week = datetime.now() - timedelta(days=7)
# this example looks at the previous 7 days of events by providing a `since` argument set to last week's date in ISO format
events_list = smartsheet_client.Events.list_events(since=last_week.isoformat(), max_count=1000)
print_new_sheet_events_in_list(events_list)

# continue listing events in the stream by using the stream_position, if the previous response indicates that more
# data is available.
while events_list.more_available:
    events_list = smartsheet_client.Events.list_events(stream_position=events_list.next_stream_position, max_count=10000,
                                        numeric_dates=True)
    print_new_sheet_events_in_list(events_list)
```

## Working with Smartsheetgov.com Accounts

If you need to access Smartsheetgov you will need to specify the Smartsheetgov API URI as the base URI during creation
of the Smartsheet client object. Smartsheetgov uses a base URI of <https://api.smartsheetgov.com/2.0/>. The base URI is
defined as a constant (`smartsheet.__gov_base__`).

You can create a client using the Smartsheetgov.com URI using the api_base parameter:

```python
client = smartsheet.Smartsheet(api_base=smartsheet.__gov_base__)
```

## Working With Smartsheet Regions Europe Accounts

If you need to access Smartsheet Regions Europe you will need to specify the Smartsheet.eu API URI as the base URI during creation of the Smartsheet client object. Smartsheet.eu uses a base URI of <https://api.smartsheet.eu/2.0/>. The base URI is defined as a constant (`smartsheet._eu_base_`).

You can create a client using the Smartsheet.eu URI using the api_base parameter:

```python
client = smartsheet.Smartsheet(api_base=smartsheet._eu_base_)
```
