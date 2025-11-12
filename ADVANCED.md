# Advanced Topics for the Smartsheet SDK for Python

## Manual install

The following packages are required.

- [setuptools](https://pypi.org/project/setuptools/)
- [six](https://pypi.python.org/pypi/six)
- [requests](https://pypi.python.org/pypi/requests)

To install this SDK manually:

1. Clone the source code from this repo [GitHub](https://github.com/smartsheet-python-sdk)
2. Install the required packages:

   ```bash
   pip install setuptools six requests
   ```

3. Ensure you are in the `smartsheet-python-sdk` directory
4. Install it using setup.py:

   ```bash
   python setup.py install
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

### Mock API Tests

We use WireMock for API contract testing. This allows us to simulate Smartsheet API responses and run tests without relying on the live API.
The [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests) repo provides a standalone WireMock server with JSON mappings that simulate the Smartsheet API.
Each mapping defines a request to match and a response to return.

Common test cases use catch-all path patterns (e.g., /errors/500-response).

We use two custom headers:

- x-test-name: Used for exact mapping match, allowing different mock responses for the same HTTP method and endpoint.
- x-request-id: A UUID generated for each request, used to verify request URLs and search for requests in WireMock admin history.

To run the mock API tests:

1. Clone the [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests) repo and follow the instructions from the readme to start the mock server.

2. `pytest tests/mock_api`

To add new mock API tests:

1. Add a WireMock Mapping (JSON) in the [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests):

```json
{
  "request": {
    "urlPathTemplate": "/2.0/users/{userId}/plans",
    "method": "GET",
    "headers": {
      "Authorization": {
        "matches": "Bearer .*"
      },
      "x-test-name": {
        "equalTo": "/users/list-user-plans/all-response-body-properties"
      },
      "x-request-id": {
        "matches": ".*"
      }
    }
  },
  "response": {
    "statusMessage": "OK",
    "status": 200,
    "jsonBody": {
      "lastKey": "12345678901234569",
      "data": [
        {
          "planId": 1234567890123456,
          "seatType": "MEMBER",
          "seatTypeLastChangedAt": "2025-01-01T00:00:00.123456789Z",
          "provisionalExpirationDate": "2026-12-13T12:17:52.525696Z",
          "isInternal": false
        }
      ]
    },
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

<!-- markdownlint-disable MD029 -->
2. Write a Test in the SDK:
<!-- markdownlint-enable MD029 -->

- Always use x-test-name to target specific mock responses.
- Use x-request-id for traceability in WireMock admin.
- Keep mappings in the smartsheet-sdk-tests repository organized and descriptive

```python
    def test_list_user_plans_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-user-plans/all-response-body-properties", request_id
    )

    response = client.Users.list_user_plans(
        user_id=TEST_USER_ID,
        last_key=TEST_LAST_KEY,
        max_items=TEST_MAX_ITEMS
    )

    assert isinstance(response, TokenPaginatedResult)
```

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
