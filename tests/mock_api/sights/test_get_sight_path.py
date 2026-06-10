import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error
from smartsheet.models.sight_path_node import SightPathNode
from tests.mock_api.common_test_constants import (
    TEST_WORKSPACE_ACCESS_LEVEL,
    TEST_WORKSPACE_ID,
    TEST_WORKSPACE_NAME,
    TEST_WORKSPACE_PERMALINK,
    TEST_PATH_FOLDER_ID,
    TEST_PATH_FOLDER_NAME,
    TEST_PATH_FOLDER_PERMALINK,
    TEST_PATH_SUBFOLDER_ID,
    TEST_PATH_SUBFOLDER_NAME,
    TEST_PATH_SUBFOLDER_PERMALINK,
    TEST_PATH_LEAF_CREATED_AT,
    TEST_PATH_LEAF_MODIFIED_AT,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

TEST_SIGHT_ID = 1234567890

TEST_PATH_SIGHT_ID = 3456789012345678
TEST_PATH_SIGHT_NAME = "Project Dashboard"
TEST_PATH_SIGHT_ACCESS_LEVEL = "ADMIN"
TEST_PATH_SIGHT_PERMALINK = "https://app.smartsheet.com/dashboards/3456789012345678"

TEST_PATH_ROOT_SIGHT_ID = 5678901234567890
TEST_PATH_ROOT_SIGHT_NAME = "Root Level Dashboard"
TEST_PATH_ROOT_SIGHT_ACCESS_LEVEL = "ADMIN"
TEST_PATH_ROOT_SIGHT_PERMALINK = "https://app.smartsheet.com/dashboards/rootlevel"


def test_get_sight_path_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sights/get-nested-sight-path/all-response-body-properties", request_id
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
        "/sights/get-nested-sight-path/all-response-body-properties", request_id
    )

    response = client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    assert isinstance(response, SightPathNode)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request.get("body")

    assert response.to_dict() == {
        "id": TEST_WORKSPACE_ID,
        "name": TEST_WORKSPACE_NAME,
        "permalink": TEST_WORKSPACE_PERMALINK,
        "accessLevel": TEST_WORKSPACE_ACCESS_LEVEL,
        "folders": [
            {
                "id": TEST_PATH_FOLDER_ID,
                "name": TEST_PATH_FOLDER_NAME,
                "permalink": TEST_PATH_FOLDER_PERMALINK,
                "folders": [
                    {
                        "id": TEST_PATH_SUBFOLDER_ID,
                        "name": TEST_PATH_SUBFOLDER_NAME,
                        "permalink": TEST_PATH_SUBFOLDER_PERMALINK,
                        "sights": [
                            {
                                "id": TEST_PATH_SIGHT_ID,
                                "name": TEST_PATH_SIGHT_NAME,
                                "permalink": TEST_PATH_SIGHT_PERMALINK,
                                "accessLevel": TEST_PATH_SIGHT_ACCESS_LEVEL,
                                "createdAt": TEST_PATH_LEAF_CREATED_AT,
                                "modifiedAt": TEST_PATH_LEAF_MODIFIED_AT,
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_get_sight_path_root_level_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sights/get-root-sight-path/all-response-body-properties", request_id
    )

    response = client.Sights.get_sight_path(sight_id=TEST_SIGHT_ID)

    assert isinstance(response, SightPathNode)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request.get("body")

    assert response.to_dict() == {
        "id": TEST_WORKSPACE_ID,
        "name": TEST_WORKSPACE_NAME,
        "permalink": TEST_WORKSPACE_PERMALINK,
        "accessLevel": TEST_WORKSPACE_ACCESS_LEVEL,
        "sights": [
            {
                "id": TEST_PATH_ROOT_SIGHT_ID,
                "name": TEST_PATH_ROOT_SIGHT_NAME,
                "permalink": TEST_PATH_ROOT_SIGHT_PERMALINK,
                "accessLevel": TEST_PATH_ROOT_SIGHT_ACCESS_LEVEL,
                "createdAt": TEST_PATH_LEAF_CREATED_AT,
                "modifiedAt": TEST_PATH_LEAF_MODIFIED_AT,
            }
        ],
    }


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
