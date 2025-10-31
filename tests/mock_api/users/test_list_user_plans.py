import uuid

from urllib.parse import urlparse, parse_qs
from dateutil import parser
from smartsheet.models.enums import seat_type
from smartsheet.models.token_paginated_result import TokenPaginatedResult
from smartsheet.models.error import Error
from tests.mock_api.users.common_test_constants import TEST_USER_ID, TEST_PLAN_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

TEST_LAST_KEY = '12345678901234569'
TEST_MAX_ITEMS = 100
TEST_SEAT_TYPE = seat_type.SeatType.MEMBER

def test_list_user_plans_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-user-plans/all-response-body-properties", request_id
    )

    client.Users.list_user_plans(
        user_id=TEST_USER_ID,
        last_key=TEST_LAST_KEY,
        max_items=TEST_MAX_ITEMS
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "lastKey": [TEST_LAST_KEY],
        "maxItems": [str(TEST_MAX_ITEMS)]
    }
    assert url.path == f"/2.0/users/{TEST_USER_ID}/plans"


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
    assert response.last_key == TEST_LAST_KEY
    assert response.data[0].plan_id == TEST_PLAN_ID
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at == parser.isoparse(
        "2025-01-01T00:00:00.123456789Z")
    assert response.data[0].provisional_expiration_date == parser.isoparse(
        "2026-12-13T12:17:52.525696Z")
    assert response.data[0].is_internal is False


def test_list_user_plans_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-user-plans/required-response-body-properties", request_id
    )

    response = client.Users.list_user_plans(
        user_id=TEST_USER_ID,
        last_key=TEST_LAST_KEY,
        max_items=TEST_MAX_ITEMS
    )

    assert isinstance(response, TokenPaginatedResult)
    assert response.data[0].plan_id == TEST_PLAN_ID
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at is None
    assert response.data[0].provisional_expiration_date is None
    assert response.data[0].is_internal is False


def test_list_user_plans_error_400_response():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.list_user_plans(
        user_id=TEST_USER_ID,
        last_key=TEST_LAST_KEY,
        max_items=TEST_MAX_ITEMS
    )

    assert isinstance(response, Error)


def test_list_user_plans_error_500_reponse():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.list_user_plans(
        user_id=TEST_USER_ID,
        last_key=TEST_LAST_KEY,
        max_items=TEST_MAX_ITEMS
    )

    assert isinstance(response, Error)
