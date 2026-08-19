import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Result, UpdateReportColumnRequest
from tests.mock_api.reports.common_test_constants import (
    TEST_REPORT_ID,
    TEST_COLUMN_VIRTUAL_ID,
    TEST_SUCCESS_MESSAGE,
    TEST_RESULT_CODE,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_update_report_column_generated_url_is_correct():
    """Test that the URL is correctly generated for PUT /reports/{id}/columns/{columnVirtualId}."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-column/all-response-body-properties", request_id
    )

    report_column = UpdateReportColumnRequest({
        "title": "Updated Task Name",
        "index": 2,
        "hidden": False,
        "width": 200,
    })

    client.Reports.update_report_column(
        report_id=TEST_REPORT_ID,
        column_virtual_id=TEST_COLUMN_VIRTUAL_ID,
        report_column=report_column,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/columns/{TEST_COLUMN_VIRTUAL_ID}'
    assert wiremock_request["method"] == "PUT"


def test_update_report_column_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-column/all-response-body-properties", request_id
    )

    report_column = UpdateReportColumnRequest({
        "title": "Updated Task Name",
        "index": 2,
        "hidden": False,
        "width": 200,
    })

    response = client.Reports.update_report_column(
        report_id=TEST_REPORT_ID,
        column_virtual_id=TEST_COLUMN_VIRTUAL_ID,
        report_column=report_column,
    )

    # Type safety checks
    assert isinstance(response, Result)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = {
        "title": "Updated Task Name",
        "index": 2,
        "hidden": False,
        "width": 200,
    }
    assert actual_body == expected_body

    # Response body assertion
    expected_result = {
        "virtualId": 7001,
        "index": 2,
        "title": "Updated Task Name",
        "type": "TEXT_NUMBER",
        "primary": True,
        "width": 200,
        "hidden": False,
        "validation": True,
        "version": 0,
        "autoNumberFormat": {
            "fill": "0001",
            "prefix": "TASK-",
            "startingNumber": 1,
            "suffix": "",
        },
    }
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE,
        "result": expected_result,
        "data": expected_result,
    }


def test_update_report_column_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-column/required-response-body-properties", request_id
    )

    report_column = UpdateReportColumnRequest({
        "title": "Updated Column",
        "index": 1,
    })

    response = client.Reports.update_report_column(
        report_id=TEST_REPORT_ID,
        column_virtual_id=TEST_COLUMN_VIRTUAL_ID,
        report_column=report_column,
    )

    # Type safety checks
    assert isinstance(response, Result)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = {
        "title": "Updated Column",
        "index": 1,
    }
    assert actual_body == expected_body

    # Response body assertion
    expected_result = {
        "index": 1,
        "title": "Updated Column",
        "type": "TEXT_NUMBER",
        "primary": True,
    }
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE,
        "result": expected_result,
        "data": expected_result,
    }


def test_update_report_column_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    report_column = UpdateReportColumnRequest({
        "title": "Updated Task Name",
        "index": 2,
        "hidden": False,
        "width": 200,
    })

    response = client.Reports.update_report_column(
        report_id=TEST_REPORT_ID,
        column_virtual_id=TEST_COLUMN_VIRTUAL_ID,
        report_column=report_column,
    )

    assert isinstance(response, Error)


def test_update_report_column_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    report_column = UpdateReportColumnRequest({
        "title": "Updated Task Name",
        "index": 2,
        "hidden": False,
        "width": 200,
    })

    response = client.Reports.update_report_column(
        report_id=TEST_REPORT_ID,
        column_virtual_id=TEST_COLUMN_VIRTUAL_ID,
        report_column=report_column,
    )

    assert isinstance(response, Error)
