import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Workspace
from tests.mock_api.common_test_constants import (
    TEST_WORKSPACE_ACCESS_LEVEL,
    TEST_WORKSPACE_ID,
    TEST_WORKSPACE_NAME,
    TEST_WORKSPACE_PERMALINK,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


TEST_FOLDER_ID = 1234567890


def test_get_folder_path_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/folders/get-folder-path/all-response-body-properties", request_id
    )

    client.Folders.get_folder_path(folder_id=TEST_FOLDER_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/folders/{TEST_FOLDER_ID}/path'
    assert wiremock_request["method"] == "GET"


def test_get_folder_path_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/folders/get-folder-path/all-response-body-properties", request_id
    )

    response = client.Folders.get_folder_path(folder_id=TEST_FOLDER_ID)

    assert isinstance(response, Workspace)

    wiremock_request = get_wiremock_request(request_id)
    request_body = wiremock_request.get("body")
    assert not request_body

    assert response.to_dict() == {
        "id": TEST_WORKSPACE_ID,
        "name": TEST_WORKSPACE_NAME,
        "permalink": TEST_WORKSPACE_PERMALINK,
        "accessLevel": TEST_WORKSPACE_ACCESS_LEVEL,
    }


def test_get_folder_path_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Folders.get_folder_path(folder_id=TEST_FOLDER_ID)

    assert isinstance(response, Error)


def test_get_folder_path_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Folders.get_folder_path(folder_id=TEST_FOLDER_ID)

    assert isinstance(response, Error)
