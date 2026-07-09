import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, TokenPaginatedResult
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_list_report_scope_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /reports/{id}/scope."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-scope/all-response-body-properties", request_id
    )

    client.Reports.list_report_scope(report_id=TEST_REPORT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/scope'
    assert wiremock_request["method"] == "GET"


def test_list_report_scope_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-scope/all-response-body-properties", request_id
    )

    response = client.Reports.list_report_scope(report_id=TEST_REPORT_ID)

    # Type safety checks
    assert isinstance(response, TokenPaginatedResult)

    # Request body assertion (GET has no body)
    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    # Response body assertion
    assert response.to_dict() == {
        "data": [
            {"assetId": 2331373580117892, "assetType": "sheet"},
            {"assetId": 7879278542455688, "assetType": "workspace"},
            {"assetId": 1234567890123456, "assetType": "sheet"},
        ]
    }


def test_list_report_scope_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/list-report-scope/required-response-body-properties", request_id
    )

    response = client.Reports.list_report_scope(report_id=TEST_REPORT_ID)

    # Type safety checks
    assert isinstance(response, TokenPaginatedResult)

    # Response body assertion
    assert response.to_dict() == {
        "data": [
            {"assetId": 2331373580117892, "assetType": "sheet"},
        ]
    }


def test_list_report_scope_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.list_report_scope(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)


def test_list_report_scope_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.list_report_scope(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)
