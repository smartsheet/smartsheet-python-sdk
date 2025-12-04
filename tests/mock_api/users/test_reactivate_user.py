import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from tests.mock_api.users.common_test_constants import TEST_USER_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_reactivate_user_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/reactivate-user/all-response-body-properties", request_id
    )

    client.Users.reactivate_user(
        user_id=TEST_USER_ID,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/users/{TEST_USER_ID}/reactivate'


def test_reactivate_user_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/users/reactivate-user/all-response-body-properties", request_id
    )

    response = client.Users.reactivate_user(
        user_id=TEST_USER_ID,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE


def test_reactivate_user_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Users.reactivate_user(
        user_id=TEST_USER_ID,
    )

    assert isinstance(response, Error)


def test_reactivate_user_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Users.reactivate_user(
        user_id=TEST_USER_ID,
    )

    assert isinstance(response, Error)
