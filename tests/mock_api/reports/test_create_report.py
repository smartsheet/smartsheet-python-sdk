import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import (
    CreateReportRequest,
    CreateReportResult,
    Error,
    Result,
)
from smartsheet.models.enums.column_type import ColumnType
from smartsheet.models.enums.report_asset_type import ReportAssetType
from smartsheet.models.enums.report_destination_type import ReportDestinationType
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


# IDs match WireMock create-report fixtures, not common_test_constants.
TEST_REPORT_ID = 987654321
TEST_REPORT_NAME = "Q2 Earnings Report"
TEST_FOLDER_ID = 3734508208295812
TEST_SHEET_ID = 4583173393803140
TEST_PERMALINK = "https://app.smartsheet.com/reports/c8gJxw87cXpRCvCC5PPw6jFhFRrf5r8PxCrxvW21"
TEST_ACCESS_LEVEL = "OWNER"


def test_create_report_generated_url_is_correct():
    """Test that the URL is correctly generated for POST /reports."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/create-report/all-response-body-properties", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.FOLDER,
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.SHEET,
                "assetId": TEST_SHEET_ID
            }
        ]
    })

    client.Reports.create_report(request)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == '/2.0/reports'
    assert wiremock_request["method"] == "POST"


def test_create_report_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/create-report/all-response-body-properties", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.FOLDER,
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0,
                "primary": True
            },
            {
                "title": "Status",
                "type": ColumnType.PICKLIST,
                "index": 1
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.SHEET,
                "assetId": TEST_SHEET_ID
            }
        ],
        "isSummaryReport": False
    })

    response = client.Reports.create_report(request)

    # Type safety checks
    assert isinstance(response, Result)
    assert isinstance(response.result, CreateReportResult)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = {
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": "folder",
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": "TEXT_NUMBER",
                "index": 0,
                "primary": True
            },
            {
                "title": "Status",
                "type": "PICKLIST",
                "index": 1
            }
        ],
        "scope": [
            {
                "assetType": "sheet",
                "assetId": TEST_SHEET_ID
            }
        ],
        "isSummaryReport": False
    }
    assert actual_body == expected_body

    # Response body assertion
    expected_result = {
        "id": TEST_REPORT_ID,
        "name": TEST_REPORT_NAME,
        "accessLevel": TEST_ACCESS_LEVEL,
        "permalink": TEST_PERMALINK,
        "isSummaryReport": False,
        "columns": [
            {
                "hidden": False,
                "index": 0,
                "primary": True,
                "title": "Primary column",
                "type": "TEXT_NUMBER",
                "validation": False,
                "version": 0,
                "virtualId": 1234567890123456,
                "width": 200
            },
            {
                "hidden": False,
                "index": 1,
                "sheetNameColumn": True,
                "title": "Sheet name",
                "type": "TEXT_NUMBER",
                "validation": False,
                "version": 0,
                "virtualId": 2345678901234567,
                "width": 150
            },
            {
                "hidden": False,
                "index": 2,
                "systemColumnType": "CREATED_DATE",
                "title": "Created at",
                "type": "DATETIME",
                "validation": False,
                "version": 0,
                "virtualId": 3456789012345678,
                "width": 150
            },
            {
                "hidden": False,
                "index": 3,
                "title": "Selected item",
                "type": "PICKLIST",
                "validation": False,
                "version": 0,
                "virtualId": 4567890123456789,
                "width": 150
            }
        ]
    }
    assert response.to_dict() == {
        "message": "SUCCESS",
        "resultCode": 0,
        "result": expected_result,
        "data": expected_result,
    }


def test_create_report_required_response_properties():
    """Test that required response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/create-report/required-response-body-properties", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.FOLDER,
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.SHEET,
                "assetId": TEST_SHEET_ID
            }
        ]
    })

    response = client.Reports.create_report(request)

    # Type safety checks
    assert isinstance(response, Result)
    assert isinstance(response.result, CreateReportResult)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = {
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": "folder",
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": "TEXT_NUMBER",
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": "sheet",
                "assetId": TEST_SHEET_ID
            }
        ]
    }
    assert actual_body == expected_body

    # Response body assertion
    expected_result = {
        "id": TEST_REPORT_ID,
        "name": TEST_REPORT_NAME,
        "accessLevel": TEST_ACCESS_LEVEL,
        "permalink": TEST_PERMALINK,
    }
    assert response.to_dict() == {
        "message": "SUCCESS",
        "resultCode": 0,
        "result": expected_result,
        "data": expected_result,
    }


def test_create_report_with_definition():
    """Test creating a report with a report definition."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/create-report/all-response-body-properties", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.WORKSPACE,
            "destinationId": 1234567890
        },
        "columns": [
            {
                "title": "Task Name",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.WORKSPACE,
                "assetId": 9876543210
            }
        ],
        "reportDefinition": {
            "filters": {
                "operator": "AND",
                "criteria": [
                    {
                        "column": {
                            "title": "Status",
                            "type": ColumnType.PICKLIST
                        },
                        "operator": "EQUAL",
                        "values": ["Complete"]
                    }
                ]
            }
        }
    })

    response = client.Reports.create_report(request)

    assert isinstance(response, Result)
    assert isinstance(response.result, CreateReportResult)

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    assert actual_body == {
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": "workspace",
            "destinationId": 1234567890
        },
        "columns": [
            {
                "title": "Task Name",
                "type": "TEXT_NUMBER",
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": "workspace",
                "assetId": 9876543210
            }
        ],
        "reportDefinition": {
            "filters": {
                "operator": "AND",
                "criteria": [
                    {
                        "column": {
                            "title": "Status",
                            "type": "PICKLIST"
                        },
                        "operator": "EQUAL",
                        "values": ["Complete"]
                    }
                ]
            }
        }
    }

    expected_result = {
        "id": TEST_REPORT_ID,
        "name": TEST_REPORT_NAME,
        "accessLevel": TEST_ACCESS_LEVEL,
        "permalink": TEST_PERMALINK,
        "isSummaryReport": False,
        "columns": [
            {
                "hidden": False,
                "index": 0,
                "primary": True,
                "title": "Primary column",
                "type": "TEXT_NUMBER",
                "validation": False,
                "version": 0,
                "virtualId": 1234567890123456,
                "width": 200
            },
            {
                "hidden": False,
                "index": 1,
                "sheetNameColumn": True,
                "title": "Sheet name",
                "type": "TEXT_NUMBER",
                "validation": False,
                "version": 0,
                "virtualId": 2345678901234567,
                "width": 150
            },
            {
                "hidden": False,
                "index": 2,
                "systemColumnType": "CREATED_DATE",
                "title": "Created at",
                "type": "DATETIME",
                "validation": False,
                "version": 0,
                "virtualId": 3456789012345678,
                "width": 150
            },
            {
                "hidden": False,
                "index": 3,
                "title": "Selected item",
                "type": "PICKLIST",
                "validation": False,
                "version": 0,
                "virtualId": 4567890123456789,
                "width": 150
            }
        ]
    }
    assert response.to_dict() == {
        "message": "SUCCESS",
        "resultCode": 0,
        "result": expected_result,
        "data": expected_result,
    }


def test_create_report_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.FOLDER,
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.SHEET,
                "assetId": TEST_SHEET_ID
            }
        ]
    })

    response = client.Reports.create_report(request)

    assert isinstance(response, Error)


def test_create_report_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    request = CreateReportRequest({
        "name": TEST_REPORT_NAME,
        "destination": {
            "destinationType": ReportDestinationType.FOLDER,
            "destinationId": TEST_FOLDER_ID
        },
        "columns": [
            {
                "title": "Primary Column",
                "type": ColumnType.TEXT_NUMBER,
                "index": 0
            }
        ],
        "scope": [
            {
                "assetType": ReportAssetType.SHEET,
                "assetId": TEST_SHEET_ID
            }
        ]
    })

    response = client.Reports.create_report(request)

    assert isinstance(response, Error)
