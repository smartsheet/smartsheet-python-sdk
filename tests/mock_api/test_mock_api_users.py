import uuid

from urllib.parse import urlparse, parse_qs
from dateutil import parser
from smartsheet.models.enums import seat_type
from smartsheet.models.index_result import IndexResult
from smartsheet.models.token_paginated_result import TokenPaginatedResult
from smartsheet.models.error import Error
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

ID = 12345678
PLAN_ID = 1234567890123456
LAST_KEY = '12345678901234569'
MAX_ITEMS = 100
EMAIL = "test.user@smartsheet.com"
TEST_SEAT_TYPE = seat_type.SeatType.MEMBER
PAGE = 1
PAGE_SIZE = 100
INCLUDE_ALL = False
FIRST_NAME = "Test"
LAST_NAME = "User"
NAME = "Test User"
ADMIN = True
LICENSED_SHEET_CREATOR = True
RESOURCE_VIEWER = True
GROUP_ADMIN = True
STATUS = "ACTIVE"
SHEET_COUNT = -1
ID_VALUE = PLAN_ID
SEAT_TYPE_LAST_CHANGED_AT = parser.isoparse("2025-06-14T09:55:30Z")
PROVISIONAL_EXPIRATION_DATE = parser.isoparse("2026-12-13T12:17:52.525696Z")
IS_INTERNAL_TRUE = True
IS_INTERNAL_FALSE = False
LAST_LOGIN = parser.isoparse("2020-10-04T18:32:47Z")
CUSTOM_WELCOME_SCREEN_VIEWED = parser.isoparse("2020-08-25T12:15:47Z")


def test_list_user_plans_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-user-plans/all-response-body-properties", request_id
    )

    client.Users.list_user_plans(
        user_id=ID,
        last_key=LAST_KEY,
        max_items=MAX_ITEMS
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "lastKey": [LAST_KEY],
        "maxItems": [str(MAX_ITEMS)]
    }
    assert url.path == f"/2.0/users/{ID}/plans"


def test_list_user_plans_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-user-plans/all-response-body-properties", request_id
    )

    response = client.Users.list_user_plans(
        user_id=ID,
        last_key=LAST_KEY,
        max_items=MAX_ITEMS
    )

    assert isinstance(response, TokenPaginatedResult)
    assert response.last_key == LAST_KEY
    assert response.data[0].plan_id == PLAN_ID
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
        user_id=ID,
        last_key=LAST_KEY,
        max_items=MAX_ITEMS
    )

    assert isinstance(response, TokenPaginatedResult)
    assert response.data[0].plan_id == PLAN_ID
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
        user_id=ID,
        last_key=LAST_KEY,
        max_items=MAX_ITEMS
    )

    assert isinstance(response, Error)


def test_list_user_plans_error_500_reponse():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.list_user_plans(
        user_id=ID,
        last_key=LAST_KEY,
        max_items=MAX_ITEMS
    )

    assert isinstance(response, Error)


def test_list_users_generated_url_is_correct():
    request_id = uuid.uuid4().hex

    client = get_mock_api_client(
        "/users/list-users/required-response-body-properties", request_id
    )

    client.Users.list_users(
        email=EMAIL,
        seat_type=TEST_SEAT_TYPE.value,
        page=PAGE,
        page_size=PAGE_SIZE,
        include_all=INCLUDE_ALL
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "email": [EMAIL],
        "seatType": [TEST_SEAT_TYPE.value],
        "page": [str(PAGE)],
        "pageSize": [str(PAGE_SIZE)],
        "includeAll": [str(INCLUDE_ALL)]
    }
    assert url.path == "/2.0/users"


def test_list_users_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-users/all-response-body-properties", request_id
    )

    response = client.Users.list_users(
        plan_id=PLAN_ID
    )

    assert isinstance(response, IndexResult)
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at == SEAT_TYPE_LAST_CHANGED_AT
    assert response.data[0].provisional_expiration_date == PROVISIONAL_EXPIRATION_DATE
    assert response.data[0].is_internal is IS_INTERNAL_TRUE
    assert response.data[0].first_name == FIRST_NAME
    assert response.data[0].last_name == LAST_NAME
    assert response.data[0].name == NAME
    assert response.data[0].email == EMAIL
    assert response.data[0].admin is ADMIN
    assert response.data[0].licensed_sheet_creator is LICENSED_SHEET_CREATOR
    assert response.data[0].resource_viewer is RESOURCE_VIEWER
    assert response.data[0].group_admin is GROUP_ADMIN
    assert response.data[0].status == STATUS
    assert response.data[0].sheet_count == SHEET_COUNT
    assert response.data[0].last_login == LAST_LOGIN
    assert response.data[0].custom_welcome_screen_viewed == CUSTOM_WELCOME_SCREEN_VIEWED
    assert response.data[0].id == ID_VALUE


def test_list_users_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-users/required-response-body-properties", request_id
    )

    response = client.Users.list_users(
        plan_id=PLAN_ID
    )

    assert isinstance(response, IndexResult)
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at is None
    assert response.data[0].provisional_expiration_date is None
    assert response.data[0].is_internal is IS_INTERNAL_TRUE
    assert response.data[0].first_name == FIRST_NAME
    assert response.data[0].last_name == LAST_NAME
    assert response.data[0].name == NAME
    assert response.data[0].email == EMAIL
    assert response.data[0].admin is ADMIN
    assert response.data[0].licensed_sheet_creator is LICENSED_SHEET_CREATOR
    assert response.data[0].resource_viewer is RESOURCE_VIEWER
    assert response.data[0].group_admin is GROUP_ADMIN
    assert response.data[0].status == STATUS
    assert response.data[0].sheet_count == SHEET_COUNT
    assert response.data[0].last_login is None
    assert response.data[0].custom_welcome_screen_viewed is None
    assert response.data[0].id == ID_VALUE


def test_list_users_error_400_response():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.list_users(
        plan_id=PLAN_ID
    )

    assert isinstance(response, Error)


def test_list_users_error_500_response():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.list_users(
        plan_id=PLAN_ID
    )

    assert isinstance(response, Error)
