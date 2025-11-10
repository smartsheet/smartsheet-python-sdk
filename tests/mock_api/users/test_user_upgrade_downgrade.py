import json
import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from smartsheet.models.enums import UpgradeSeatType, DowngradeSeatType
from tests.mock_api.users.common_test_constants import TEST_USER_ID, TEST_PLAN_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

TEST_UPGRADE_SEAT_TYPE = UpgradeSeatType.MEMBER
TEST_DOWNGRADE_SEAT_TYPE = DowngradeSeatType.VIEWER


def test_upgrade_user_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/upgrade-user/all-response-body-properties", request_id
    )

    client.Users.upgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_UPGRADE_SEAT_TYPE,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/users/{TEST_USER_ID}/plans/{TEST_PLAN_ID}/upgrade'


def test_upgrade_user_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/upgrade-user/all-response-body-properties", request_id
    )

    response = client.Users.upgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_UPGRADE_SEAT_TYPE,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {"seatType": TEST_UPGRADE_SEAT_TYPE.value}

def test_upgrade_user_no_seat_type():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/upgrade-user/all-response-body-properties", request_id
    )

    response = client.Users.upgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=None,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {"seatType": None}

def test_upgrade_user_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.upgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_UPGRADE_SEAT_TYPE,
    )

    assert isinstance(response, Error)


def test_upgrade_user_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.upgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_UPGRADE_SEAT_TYPE,
    )

    assert isinstance(response, Error)


def test_downgrade_user_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/downgrade-user/all-response-body-properties", request_id
    )

    client.Users.downgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_DOWNGRADE_SEAT_TYPE,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/users/{TEST_USER_ID}/plans/{TEST_PLAN_ID}/downgrade'


def test_downgrade_user_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/downgrade-user/all-response-body-properties", request_id
    )

    response = client.Users.downgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_DOWNGRADE_SEAT_TYPE,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {"seatType": TEST_DOWNGRADE_SEAT_TYPE.value}


def test_downgrade_user_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.downgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_DOWNGRADE_SEAT_TYPE,
    )

    assert isinstance(response, Error)


def test_downgrade_user_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.downgrade_user(
        user_id=TEST_USER_ID,
        plan_id=TEST_PLAN_ID,
        seat_type=TEST_DOWNGRADE_SEAT_TYPE,
    )

    assert isinstance(response, Error)
