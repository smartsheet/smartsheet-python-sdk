import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error, Result, ReportScopeInclusion
from smartsheet.models.enums.report_asset_type import ReportAssetType
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID, TEST_SHEET_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_add_report_scope_generated_url_is_correct():
    """Test that the URL is correctly generated for POST /reports/{id}/scope."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/add-report-scope/all-response-body-properties", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    client.Reports.add_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/scope'
    assert wiremock_request["method"] == "POST"


def test_add_report_scope_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/add-report-scope/all-response-body-properties", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    response = client.Reports.add_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    # Type safety checks
    assert isinstance(response, Result)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    expected_body = [
        {
            "assetId": TEST_SHEET_ID,
            "assetType": "sheet"
        }
    ]
    assert actual_body == expected_body

    # Response body assertion
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE
    }


def test_add_report_scope_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    response = client.Reports.add_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    assert isinstance(response, Error)


def test_add_report_scope_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    response = client.Reports.add_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    assert isinstance(response, Error)
