import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error
from smartsheet.models.sheet_path_node import SheetPathNode
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

TEST_SHEET_ID = 1234567890

TEST_PATH_SHEET_ID = 3456789012345678
TEST_PATH_SHEET_NAME = "Project Plan"
TEST_PATH_SHEET_ACCESS_LEVEL = "ADMIN"
TEST_PATH_SHEET_PERMALINK = "https://app.smartsheet.com/sheets/3456789012345678"

TEST_PATH_ROOT_SHEET_ID = 5678901234567890
TEST_PATH_ROOT_SHEET_NAME = "Root Level Sheet"
TEST_PATH_ROOT_SHEET_ACCESS_LEVEL = "ADMIN"
TEST_PATH_ROOT_SHEET_PERMALINK = "https://app.smartsheet.com/sheets/rootlevel"


def test_get_sheet_path_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/get-nested-sheet-path/all-response-body-properties", request_id
    )

    client.Sheets.get_sheet_path(sheet_id=TEST_SHEET_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/sheets/{TEST_SHEET_ID}/path'
    assert wiremock_request["method"] == "GET"


def test_get_sheet_path_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/get-nested-sheet-path/all-response-body-properties", request_id
    )

    response = client.Sheets.get_sheet_path(sheet_id=TEST_SHEET_ID)

    assert isinstance(response, SheetPathNode)

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
                        "sheets": [
                            {
                                "id": TEST_PATH_SHEET_ID,
                                "name": TEST_PATH_SHEET_NAME,
                                "permalink": TEST_PATH_SHEET_PERMALINK,
                                "accessLevel": TEST_PATH_SHEET_ACCESS_LEVEL,
                                "createdAt": TEST_PATH_LEAF_CREATED_AT,
                                "modifiedAt": TEST_PATH_LEAF_MODIFIED_AT,
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_get_sheet_path_root_level_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/get-root-sheet-path/all-response-body-properties", request_id
    )

    response = client.Sheets.get_sheet_path(sheet_id=TEST_SHEET_ID)

    assert isinstance(response, SheetPathNode)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request.get("body")

    assert response.to_dict() == {
        "id": TEST_WORKSPACE_ID,
        "name": TEST_WORKSPACE_NAME,
        "permalink": TEST_WORKSPACE_PERMALINK,
        "accessLevel": TEST_WORKSPACE_ACCESS_LEVEL,
        "sheets": [
            {
                "id": TEST_PATH_ROOT_SHEET_ID,
                "name": TEST_PATH_ROOT_SHEET_NAME,
                "permalink": TEST_PATH_ROOT_SHEET_PERMALINK,
                "accessLevel": TEST_PATH_ROOT_SHEET_ACCESS_LEVEL,
                "createdAt": TEST_PATH_LEAF_CREATED_AT,
                "modifiedAt": TEST_PATH_LEAF_MODIFIED_AT,
            }
        ],
    }


def test_get_sheet_path_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sheets.get_sheet_path(sheet_id=TEST_SHEET_ID)

    assert isinstance(response, Error)


def test_get_sheet_path_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sheets.get_sheet_path(sheet_id=TEST_SHEET_ID)

    assert isinstance(response, Error)
