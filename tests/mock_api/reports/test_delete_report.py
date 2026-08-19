import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Result
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_delete_report_generated_url_is_correct():
    """Test that the URL is correctly generated for DELETE /reports/{id}."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/delete-report/all-response-body-properties", request_id
    )

    client.Reports.delete_report(report_id=TEST_REPORT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}'
    assert wiremock_request["method"] == "DELETE"


def test_delete_report_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/delete-report/all-response-body-properties", request_id
    )

    response = client.Reports.delete_report(report_id=TEST_REPORT_ID)

    # Type safety checks
    assert isinstance(response, Result)

    # Request body assertion (DELETE has no body)
    wiremock_request = get_wiremock_request(request_id)
    request_body = wiremock_request.get("body")
    assert not request_body

    # Response body assertion
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE
    }


def test_delete_report_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.delete_report(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)


def test_delete_report_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.delete_report(report_id=TEST_REPORT_ID)

    assert isinstance(response, Error)
