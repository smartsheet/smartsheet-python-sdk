import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, ReportColumn
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_get_report_column_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /reports/{id}/columns/{columnVirtualId}."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-report-column/all-response-body-properties", request_id
    )

    client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/columns/{TEST_COLUMN_VIRTUAL_ID}'
    assert wiremock_request["method"] == "GET"


def test_get_report_column_with_level_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /reports/{id}/columns/{columnVirtualId}."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-report-column/all-response-body-properties", request_id
    )

    client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID, 3)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert query == {
        "level": "3"
    }

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/columns/{TEST_COLUMN_VIRTUAL_ID}'
    assert wiremock_request["method"] == "GET"


def test_get_report_column_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-report-column/all-response-body-properties", request_id
    )

    response = client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID)

    # Type safety checks
    assert isinstance(response, ReportColumn)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    # Response body assertion
    assert response.to_dict() == {
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
    }


def test_get_report_column_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/get-report-column/required-response-body-properties", request_id
    )

    response = client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID)

    # Type safety checks
    assert isinstance(response, ReportColumn)

    # Response body assertion
    assert response.to_dict() == {
        "index": 0,
        "title": "Task Name",
        "type": "TEXT_NUMBER",
        "primary": True
    }


def test_get_report_column_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID)

    assert isinstance(response, Error)


def test_get_report_column_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.get_report_column(TEST_REPORT_ID, TEST_COLUMN_VIRTUAL_ID)

    assert isinstance(response, Error)
