import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, TokenPaginatedResult
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_list_report_columns_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /reports/{id}/columns."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-columns/all-response-body-properties", request_id
    )

    client.Reports.list_report_columns(report_id=TEST_REPORT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/columns'
    assert wiremock_request["method"] == "GET"


def test_list_report_columns_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-columns/all-response-body-properties", request_id
    )

    response = client.Reports.list_report_columns(report_id=TEST_REPORT_ID)

    # Type safety checks
    assert isinstance(response, TokenPaginatedResult)

    # Request body assertion (GET has no body)
    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    # Response body assertion
    assert response.to_dict() == {
        "data": [
            {
                "virtualId": 7001,
                "index": 0,
                "title": "Task Name",
                "type": "TEXT_NUMBER",
                "primary": True,
                "width": 150,
                "hidden": False,
                "validation": True,
                "version": 0,
                "autoNumberFormat": {
                    "fill": "0001",
                    "prefix": "TASK-",
                    "startingNumber": 1,
                    "suffix": ""
                }
            },
            {
                "virtualId": 7002,
                "index": 1,
                "title": "Status",
                "type": "PICKLIST",
                "width": 120,
                "hidden": False,
                "validation": False,
                "version": 0
            },
            {
                "virtualId": 7003,
                "index": 2,
                "title": "Created By",
                "type": "CONTACT_LIST",
                "systemColumnType": "CREATED_BY",
                "width": 150,
                "hidden": False,
                "validation": False,
                "version": 1
            },
            {
                "virtualId": 7004,
                "index": 3,
                "title": "Sheet Name",
                "type": "TEXT_NUMBER",
                "sheetNameColumn": True,
                "width": 200,
                "hidden": False,
                "validation": False,
                "version": 0
            }
        ]
    }


def test_list_report_columns_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-columns/required-response-body-properties", request_id
    )

    response = client.Reports.list_report_columns(report_id=TEST_REPORT_ID)

    # Type safety checks
    assert isinstance(response, TokenPaginatedResult)

    # Response body assertion
    assert response.to_dict() == {
        "data": [
            {
                "index": 0,
                "title": "Task Name",
                "type": "TEXT_NUMBER",
                "primary": True
            },
            {
                "index": 1,
                "type": "DATETIME",
                "systemColumnType": "CREATED_DATE"
            }
        ]
    }


def test_list_report_columns_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.list_report_columns(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)


def test_list_report_columns_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.list_report_columns(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)
