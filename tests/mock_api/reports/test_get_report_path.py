import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error
from smartsheet.models.report_path_node import ReportPathNode
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
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID

TEST_PATH_REPORT_ID = 3456789012345678
TEST_PATH_REPORT_NAME = "Project Report"
TEST_PATH_REPORT_ACCESS_LEVEL = "ADMIN"
TEST_PATH_REPORT_PERMALINK = "https://app.smartsheet.com/reports/3456789012345678"

TEST_PATH_ROOT_REPORT_ID = 5678901234567890
TEST_PATH_ROOT_REPORT_NAME = "Root Level Report"
TEST_PATH_ROOT_REPORT_ACCESS_LEVEL = "ADMIN"
TEST_PATH_ROOT_REPORT_PERMALINK = "https://app.smartsheet.com/reports/rootlevel"


def test_get_report_path_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-nested-report-path/all-response-body-properties", request_id
    )

    client.Reports.get_report_path(report_id=TEST_REPORT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/path'
    assert wiremock_request["method"] == "GET"


def test_get_report_path_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-nested-report-path/all-response-body-properties", request_id
    )

    response = client.Reports.get_report_path(report_id=TEST_REPORT_ID)

    assert isinstance(response, ReportPathNode)

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
                        "reports": [
                            {
                                "id": TEST_PATH_REPORT_ID,
                                "name": TEST_PATH_REPORT_NAME,
                                "permalink": TEST_PATH_REPORT_PERMALINK,
                                "accessLevel": TEST_PATH_REPORT_ACCESS_LEVEL,
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_get_report_path_root_level_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-root-report-path/all-response-body-properties", request_id
    )

    response = client.Reports.get_report_path(report_id=TEST_REPORT_ID)

    assert isinstance(response, ReportPathNode)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request.get("body")

    assert response.to_dict() == {
        "id": TEST_WORKSPACE_ID,
        "name": TEST_WORKSPACE_NAME,
        "permalink": TEST_WORKSPACE_PERMALINK,
        "accessLevel": TEST_WORKSPACE_ACCESS_LEVEL,
        "reports": [
            {
                "id": TEST_PATH_ROOT_REPORT_ID,
                "name": TEST_PATH_ROOT_REPORT_NAME,
                "permalink": TEST_PATH_ROOT_REPORT_PERMALINK,
                "accessLevel": TEST_PATH_ROOT_REPORT_ACCESS_LEVEL,
            }
        ],
    }


def test_get_report_path_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.get_report_path(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)


def test_get_report_path_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.get_report_path(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)
