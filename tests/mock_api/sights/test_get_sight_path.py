import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Workspace
from tests.mock_api.common_test_constants import (
    TEST_WORKSPACE_ACCESS_LEVEL,
    TEST_WORKSPACE_ID,
    TEST_WORKSPACE_NAME,
    TEST_WORKSPACE_PERMALINK,
    TEST_PATH_FOLDER_ID,
    TEST_PATH_FOLDER_NAME,
    TEST_PATH_SHEET_ID,
    TEST_PATH_SHEET_NAME,
    TEST_PATH_SHEET_ACCESS_LEVEL,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


TEST_SIGHT_ID = 1234567890


def test_get_sight_path_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sights/get-sight-path/all-response-body-properties", request_id
    )

    client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/sights/{TEST_SIGHT_ID}/path'
    assert wiremock_request["method"] == "GET"


def test_get_sight_path_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sights/get-sight-path/all-response-body-properties", request_id
    )

    response = client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    assert isinstance(response, Workspace)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request.get("body")

    assert response.id == TEST_WORKSPACE_ID
    assert response.name == TEST_WORKSPACE_NAME
    assert response.permalink == TEST_WORKSPACE_PERMALINK
    assert response.access_level == TEST_WORKSPACE_ACCESS_LEVEL

    assert len(response.folders) == 1
    folder = response.folders[0]
    assert folder.id == TEST_PATH_FOLDER_ID
    assert folder.name == TEST_PATH_FOLDER_NAME

    assert len(folder.sheets) == 1
    sheet = folder.sheets[0]
    assert sheet.id == TEST_PATH_SHEET_ID
    assert sheet.name == TEST_PATH_SHEET_NAME
    assert sheet.access_level == TEST_PATH_SHEET_ACCESS_LEVEL


def test_get_sight_path_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    assert isinstance(response, Error)


def test_get_sight_path_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    assert isinstance(response, Error)
