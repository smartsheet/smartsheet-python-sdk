import uuid

from urllib.parse import urlparse, parse_qs
from dateutil import parser
from smartsheet.models.enums import seat_type
from smartsheet.models.index_result import IndexResult
from smartsheet.models.error import Error
from tests.mock_api.users.common_test_constants import TEST_PLAN_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

TEST_EMAIL = "test.user@smartsheet.com"
TEST_SEAT_TYPE = seat_type.SeatType.MEMBER
TEST_PAGE = 1
TEST_PAGE_SIZE = 100
TEST_INCLUDE_ALL = False
TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "User"
TEST_NAME = "Test User"
TEST_ADMIN = True
TEST_LICENSED_SHEET_CREATOR = True
TEST_RESOURCE_VIEWER = True
TEST_GROUP_ADMIN = True
TEST_STATUS = "ACTIVE"
TEST_SHEET_COUNT = -1
TEST_ID_VALUE = TEST_PLAN_ID
TEST_SEAT_TYPE_LAST_CHANGED_AT = parser.isoparse("2025-01-01T00:00:00.123456Z")
TEST_PROVISIONAL_EXPIRATION_DATE = parser.isoparse("2026-12-13T12:17:52.525696Z")
TEST_IS_INTERNAL_TRUE = True
TEST_IS_INTERNAL_FALSE = False
TEST_LAST_LOGIN = parser.isoparse("2020-10-04T18:32:47Z")
TEST_CUSTOM_WELCOME_SCREEN_VIEWED = parser.isoparse("2020-08-25T12:15:47Z")

def test_list_users_generated_url_is_correct():
    request_id = uuid.uuid4().hex

    client = get_mock_api_client(
        "/users/list-users/required-response-body-properties", request_id
    )

    client.Users.list_users(
        email=TEST_EMAIL,
        seat_type=TEST_SEAT_TYPE.value,
        page=TEST_PAGE,
        page_size=TEST_PAGE_SIZE,
        include_all=TEST_INCLUDE_ALL
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "email": [TEST_EMAIL],
        "seatType": [TEST_SEAT_TYPE.value],
        "page": [str(TEST_PAGE)],
        "pageSize": [str(TEST_PAGE_SIZE)],
        "includeAll": [str(TEST_INCLUDE_ALL)]
    }
    assert url.path == "/2.0/users"


def test_list_users_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-users/all-response-body-properties", request_id
    )

    response = client.Users.list_users(
        plan_id=TEST_PLAN_ID
    )

    assert isinstance(response, IndexResult)
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at == TEST_SEAT_TYPE_LAST_CHANGED_AT
    assert response.data[0].provisional_expiration_date == TEST_PROVISIONAL_EXPIRATION_DATE
    assert response.data[0].is_internal is TEST_IS_INTERNAL_TRUE
    assert response.data[0].first_name == TEST_FIRST_NAME
    assert response.data[0].last_name == TEST_LAST_NAME
    assert response.data[0].name == TEST_NAME
    assert response.data[0].email == TEST_EMAIL
    assert response.data[0].admin is TEST_ADMIN
    assert response.data[0].licensed_sheet_creator is TEST_LICENSED_SHEET_CREATOR
    assert response.data[0].resource_viewer is TEST_RESOURCE_VIEWER
    assert response.data[0].group_admin is TEST_GROUP_ADMIN
    assert response.data[0].status == TEST_STATUS
    assert response.data[0].sheet_count == TEST_SHEET_COUNT
    assert response.data[0].last_login == TEST_LAST_LOGIN
    assert response.data[0].custom_welcome_screen_viewed == TEST_CUSTOM_WELCOME_SCREEN_VIEWED
    assert response.data[0].id == TEST_ID_VALUE


def test_list_users_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/list-users/required-response-body-properties", request_id
    )

    response = client.Users.list_users(
        plan_id=TEST_PLAN_ID
    )

    assert isinstance(response, IndexResult)
    assert response.data[0].seat_type == TEST_SEAT_TYPE.value
    assert response.data[0].seat_type_last_changed_at is None
    assert response.data[0].provisional_expiration_date is None
    assert response.data[0].is_internal is TEST_IS_INTERNAL_TRUE
    assert response.data[0].first_name == TEST_FIRST_NAME
    assert response.data[0].last_name == TEST_LAST_NAME
    assert response.data[0].name == TEST_NAME
    assert response.data[0].email == TEST_EMAIL
    assert response.data[0].admin is TEST_ADMIN
    assert response.data[0].licensed_sheet_creator is TEST_LICENSED_SHEET_CREATOR
    assert response.data[0].resource_viewer is TEST_RESOURCE_VIEWER
    assert response.data[0].group_admin is TEST_GROUP_ADMIN
    assert response.data[0].status == TEST_STATUS
    assert response.data[0].sheet_count == TEST_SHEET_COUNT
    assert response.data[0].last_login is None
    assert response.data[0].custom_welcome_screen_viewed is None
    assert response.data[0].id == TEST_ID_VALUE


def test_list_users_error_400_response():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.list_users(
        plan_id=TEST_PLAN_ID
    )

    assert isinstance(response, Error)


def test_list_users_error_500_response():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.list_users(
        plan_id=TEST_PLAN_ID
    )

    assert isinstance(response, Error)
