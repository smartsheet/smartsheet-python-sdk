import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, ReportColumn, Result
from smartsheet.models.enums import ColumnType
from tests.mock_api.reports.common_test_constants import (
    TEST_REPORT_ID,
    TEST_SUCCESS_MESSAGE,
    TEST_RESULT_CODE,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_add_report_columns_generated_url_is_correct():
    """Test that the URL is correctly generated for POST /reports/{id}/columns."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/add-report-columns/all-response-body-properties", request_id
    )

    columns = [
        ReportColumn({
            "title": "Item selected",
            "type": ColumnType.CHECKBOX,
            "index": 4
        }),
        ReportColumn({
            "title": "Sheet name",
            "type": ColumnType.TEXT_NUMBER,
            "index": 4
        })
    ]

    client.Reports.add_report_columns(
        report_id=TEST_REPORT_ID,
        report_columns=columns
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/columns'
    assert wiremock_request["method"] == "POST"


def test_add_report_columns_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/add-report-columns/all-response-body-properties", request_id
    )

    columns = [
        ReportColumn({
            "title": "Item selected",
            "type": ColumnType.CHECKBOX,
            "index": 4
        }),
        ReportColumn({
            "title": "Sheet name",
            "type": ColumnType.TEXT_NUMBER,
            "index": 4,
            "sheetNameColumn": True
        })
    ]

    response = client.Reports.add_report_columns(
        report_id=TEST_REPORT_ID,
        report_columns=columns
    )

    # Type safety checks
    assert isinstance(response, Result)
    assert isinstance(response.result[0], ReportColumn)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = [
        {
            "title": "Item selected",
            "type": "CHECKBOX",
            "index": 4
        },
        {
            "title": "Sheet name",
            "type": "TEXT_NUMBER",
            "index": 4,
            "sheetNameColumn": True
        }
    ]
    assert actual_body == expected_body

    # Response body assertion
    expected_columns = [
        {
            "virtualId": 12345,
            "index": 4,
            "title": "Item selected",
            "type": "CHECKBOX",
            "hidden": False,
            "version": 0,
            "width": 150,
            "validation": False
        },
        {
            "virtualId": 12346,
            "index": 5,
            "title": "Sheet name",
            "type": "TEXT_NUMBER",
            "hidden": False,
            "version": 0,
            "width": 150,
            "sheetNameColumn": True,
            "validation": False
        },
        {
            "virtualId": 12347,
            "index": 6,
            "title": "Created By",
            "type": "CONTACT_LIST",
            "systemColumnType": "CREATED_BY",
            "hidden": False,
            "version": 0,
            "width": 150,
            "validation": False
        },
        {
            "virtualId": 12348,
            "index": 7,
            "title": "Primary",
            "type": "TEXT_NUMBER",
            "primary": True,
            "hidden": False,
            "version": 0,
            "width": 200,
            "validation": False
        },
        {
            "virtualId": 12349,
            "index": 8,
            "title": "Row Number",
            "type": "TEXT_NUMBER",
            "systemColumnType": "AUTO_NUMBER",
            "hidden": False,
            "version": 0,
            "width": 100,
            "validation": False,
            "autoNumberFormat": {
                "fill": "000",
                "prefix": "TASK-",
                "startingNumber": 1,
                "suffix": ""
            }
        }
    ]
    # Verify complete response as whole object
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE,
        "result": expected_columns,
        "data": expected_columns,
    }


def test_add_report_columns_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/add-report-columns/required-response-body-properties", request_id
    )

    columns = [
        ReportColumn({
            "title": "Item selected",
            "type": ColumnType.CHECKBOX,
            "index": 4
        }),
        ReportColumn({
            "title": "Sheet name",
            "type": ColumnType.TEXT_NUMBER,
            "index": 4
        })
    ]

    response = client.Reports.add_report_columns(
        report_id=TEST_REPORT_ID,
        report_columns=columns
    )

    # Type safety checks
    assert isinstance(response, Result)
    assert isinstance(response.result[0], ReportColumn)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = [
        {
            "title": "Item selected",
            "type": "CHECKBOX",
            "index": 4
        },
        {
            "title": "Sheet name",
            "type": "TEXT_NUMBER",
            "index": 4
        }
    ]
    assert actual_body == expected_body

    # Response body assertion
    expected_columns = [
        {
            "virtualId": 12345,
            "index": 4,
            "title": "Item selected",
            "type": "CHECKBOX",
            "version": 0
        },
        {
            "virtualId": 12346,
            "index": 5,
            "title": "Sheet name",
            "type": "TEXT_NUMBER",
            "sheetNameColumn": True,
            "version": 0
        },
        {
            "virtualId": 12347,
            "index": 6,
            "title": "Created By",
            "type": "CONTACT_LIST",
            "systemColumnType": "CREATED_BY",
            "version": 0
        },
        {
            "virtualId": 12348,
            "index": 7,
            "title": "Primary",
            "type": "TEXT_NUMBER",
            "primary": True,
            "version": 0
        },
        {
            "virtualId": 12349,
            "index": 8,
            "title": "Row Number",
            "type": "TEXT_NUMBER",
            "systemColumnType": "AUTO_NUMBER",
            "version": 0,
            "autoNumberFormat": {
                "fill": "000",
                "prefix": "TASK-",
                "startingNumber": 1,
                "suffix": ""
            }
        }
    ]
    # Verify complete response as whole object
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE,
        "result": expected_columns,
        "data": expected_columns
    }


def test_add_report_columns_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    columns = [
        ReportColumn({
            "title": "Test Column",
            "type": ColumnType.TEXT_NUMBER,
            "index": 0
        })
    ]

    response = client.Reports.add_report_columns(
        report_id=TEST_REPORT_ID,
        report_columns=columns
    )

    assert isinstance(response, Error)


def test_add_report_columns_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    columns = [
        ReportColumn({
            "title": "Test Column",
            "type": ColumnType.TEXT_NUMBER,
            "index": 0
        })
    ]

    response = client.Reports.add_report_columns(
        report_id=TEST_REPORT_ID,
        report_columns=columns
    )

    assert isinstance(response, Error)
