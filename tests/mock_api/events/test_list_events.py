import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Event, EventResult

from tests.mock_api.mock_api_test_helper import get_mock_api_client, get_wiremock_request
from tests.mock_api.events.common_test_constants import (
    TEST_EVENT_ID_1,
    TEST_EVENT_ID_2,
    TEST_EVENT_ID_3,
    TEST_EVENT_ID_4,
    TEST_EVENT_ID_5,
    TEST_EVENT_TIMESTAMP_1,
    TEST_EVENT_TIMESTAMP_2,
    TEST_EVENT_TIMESTAMP_3,
    TEST_EVENT_TIMESTAMP_4,
    TEST_EVENT_TIMESTAMP_5,
    TEST_NEXT_STREAM_POSITION,
    TEST_OBJECT_ID_1,
    TEST_OBJECT_ID_2,
    TEST_OBJECT_ID_3,
    TEST_OBJECT_ID_4,
    TEST_OBJECT_ID_5,
    TEST_OBJECT_ID_STR_1,
    TEST_OBJECT_ID_STR_2,
    TEST_OBJECT_ID_STR_3,
    TEST_OBJECT_ID_STR_4,
    TEST_OBJECT_ID_STR_5,
    TEST_SINCE,
    TEST_USER_ID_1,
    TEST_USER_ID_2,
    TEST_USER_ID_3,
)

EXPECTED_ALL_RESPONSE_PROPERTIES = {
    "moreAvailable": True,
    "nextStreamPosition": TEST_NEXT_STREAM_POSITION,
    "data": [
        {
            "eventId": TEST_EVENT_ID_1,
            "objectType": "SHEET",
            "objectId": TEST_OBJECT_ID_1,
            "objectIdStr": TEST_OBJECT_ID_STR_1,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_1,
            "action": "UPDATE",
            "source": "WEB_APP",
            "additionalDetails": {"emailAddress": "test@test.com"},
        },
        {
            "eventId": TEST_EVENT_ID_2,
            "objectType": "WORKSPACE",
            "objectId": TEST_OBJECT_ID_2,
            "objectIdStr": TEST_OBJECT_ID_STR_2,
            "userId": TEST_USER_ID_2,
            "requestUserId": TEST_USER_ID_2,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_2,
            "action": "CREATE",
            "source": "API_UNDEFINED_APP",
            "additionalDetails": {"emailAddress": "test@test.com"},
        },
        {
            "eventId": TEST_EVENT_ID_3,
            "objectType": "SHEET",
            "action": "PURGE",
            "objectId": TEST_OBJECT_ID_3,
            "objectIdStr": TEST_OBJECT_ID_STR_3,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_3,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "source": "UNKNOWN",
            "additionalDetails": {"emailAddress": "test@test.com"},
        },
        {
            "eventId": TEST_EVENT_ID_4,
            "objectType": "ATTACHMENT",
            "action": "CREATE",
            "objectId": TEST_OBJECT_ID_4,
            "objectIdStr": TEST_OBJECT_ID_STR_4,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_4,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "source": "UNKNOWN",
            "additionalDetails": {
                "emailAddress": "test@test.com",
                "sheetId": "102030405",
                "attachmentName": "picture.jpg",
            },
        },
        {
            "eventId": TEST_EVENT_ID_5,
            "objectType": "SHEET",
            "action": "LOAD",
            "objectId": TEST_OBJECT_ID_5,
            "objectIdStr": TEST_OBJECT_ID_STR_5,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_5,
            "userId": TEST_USER_ID_3,
            "requestUserId": TEST_USER_ID_3,
            "source": "API_INTEGRATED_APP",
            "additionalDetails": {"emailAddress": "test@test.com"},
        },
    ],
}

EXPECTED_REQUIRED_RESPONSE_PROPERTIES = {
    "moreAvailable": False,
    "data": [
        {
            "eventId": TEST_EVENT_ID_1,
            "objectType": "SHEET",
            "objectId": TEST_OBJECT_ID_1,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_1,
            "action": "UPDATE",
            "source": "WEB_APP",
        },
        {
            "eventId": TEST_EVENT_ID_2,
            "objectType": "WORKSPACE",
            "objectId": TEST_OBJECT_ID_2,
            "userId": TEST_USER_ID_2,
            "requestUserId": TEST_USER_ID_2,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_2,
            "action": "CREATE",
            "source": "API_UNDEFINED_APP",
        },
        {
            "eventId": TEST_EVENT_ID_3,
            "objectType": "SHEET",
            "action": "PURGE",
            "objectId": TEST_OBJECT_ID_3,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_3,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "source": "UNKNOWN",
        },
        {
            "eventId": TEST_EVENT_ID_4,
            "objectType": "ATTACHMENT",
            "action": "CREATE",
            "objectId": TEST_OBJECT_ID_4,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_4,
            "userId": TEST_USER_ID_1,
            "requestUserId": TEST_USER_ID_1,
            "source": "UNKNOWN",
        },
        {
            "eventId": TEST_EVENT_ID_5,
            "objectType": "SHEET",
            "action": "LOAD",
            "objectId": TEST_OBJECT_ID_5,
            "eventTimestamp": TEST_EVENT_TIMESTAMP_5,
            "userId": TEST_USER_ID_3,
            "requestUserId": TEST_USER_ID_3,
            "source": "API_INTEGRATED_APP",
        },
    ],
}


def test_get_events_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /events."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/events/list-events/all-response-body-properties", request_id
    )

    client.Events.list_events(since=TEST_SINCE)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert query == {"since": [TEST_SINCE]}

    assert url.path == "/2.0/events"
    assert wiremock_request["method"] == "GET"


def test_get_events_all_response_properties():
    """Test that all response properties are correctly deserialized, including objectIdStr."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/events/list-events/all-response-body-properties", request_id
    )

    response = client.Events.list_events()

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert isinstance(response, EventResult)
    assert isinstance(response.data[0], Event)
    assert response.to_dict() == EXPECTED_ALL_RESPONSE_PROPERTIES


def test_get_events_required_response_properties():
    """Test that required-only response properties are correctly deserialized (no objectIdStr)."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/events/list-events/required-response-body-properties", request_id
    )

    response = client.Events.list_events()

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert isinstance(response, EventResult)
    assert isinstance(response.data[0], Event)
    assert response.to_dict() == EXPECTED_REQUIRED_RESPONSE_PROPERTIES


def test_get_events_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/400-response", request_id)

    response = client.Events.list_events()

    assert isinstance(response, Error)


def test_get_events_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/500-response", request_id)

    response = client.Events.list_events()

    assert isinstance(response, Error)
