import json
import uuid
from urllib.parse import urlparse

from smartsheet.models import (
    CreateReportRequest,
    Error,
)
from smartsheet.models.enums.access_level import AccessLevel
from smartsheet.models.enums.column_type import ColumnType
from smartsheet.models.enums.report_asset_type import ReportAssetType
from smartsheet.models.enums.report_destination_type import ReportDestinationType
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


# Test constants
TEST_REPORT_ID = 987654321
TEST_REPORT_NAME = "Q2 Earnings Report"
TEST_FOLDER_ID = 3734508208295812
TEST_SHEET_ID = 4583173393803140
TEST_PERMALINK = "https://app.smartsheet.com/reports/c8gJxw87cXpRCvCC5PPw6jFhFRrf5r8PxCrxvW21"


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
                "index": 0
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

    assert response.result.id == TEST_REPORT_ID
    assert response.result.name == TEST_REPORT_NAME
    assert response.result.access_level == AccessLevel.OWNER
    assert response.result.permalink == TEST_PERMALINK
    assert response.result.is_summary_report is False
    assert len(response.result.columns) == 4

    # Verify column details
    columns = response.result.columns
    assert columns[0].title == "Primary column"
    assert columns[0].primary is True
    assert columns[1].sheet_name_column is True
    assert columns[2].system_column_type == "CREATED_DATE"
    assert columns[3].title == "Selected item"


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

    assert response.result.id == TEST_REPORT_ID
    assert response.result.name == TEST_REPORT_NAME
    assert response.result.access_level == AccessLevel.OWNER
    assert response.result.permalink == TEST_PERMALINK
    assert response.result.is_summary_report is None


def test_create_report_request_body_serialization():
    """Test that request body is correctly serialized."""
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

    client.Reports.create_report(request)

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

    client.Reports.create_report(request)

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    assert "reportDefinition" in actual_body
    assert actual_body["reportDefinition"]["filters"]["operator"] == "AND"
    assert len(actual_body["reportDefinition"]["filters"]["criteria"]) == 1


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
