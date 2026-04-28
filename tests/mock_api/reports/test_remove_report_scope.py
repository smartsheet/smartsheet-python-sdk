import json
import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from smartsheet.models.enums.report_asset_type import ReportAssetType
from smartsheet.models.report_scope_inclusion import ReportScopeInclusion
from tests.mock_api.reports.common_test_constants import TEST_REPORT_ID, TEST_SHEET_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_remove_report_scope_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/remove-report-scope/all-response-body-properties", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    client.Reports.remove_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/scope'
    assert wiremock_request["method"] == "DELETE"

def test_remove_report_scope_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/remove-report-scope/all-response-body-properties", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    response = client.Reports.remove_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE


def test_remove_report_scope_request_body_serialization():
    """Test that request body is correctly serialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/remove-report-scope/all-response-body-properties", request_id
    )

    scopes = [
        ReportScopeInclusion({
            "assetId": TEST_SHEET_ID,
            "assetType": ReportAssetType.SHEET
        })
    ]

    client.Reports.remove_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    expected_body = [
        {
            "assetId": TEST_SHEET_ID,
            "assetType": "sheet"
        }
    ]

    assert actual_body == expected_body



def test_remove_report_scope_error_4xx():
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

    response = client.Reports.remove_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    assert isinstance(response, Error)


def test_remove_report_scope_error_5xx():
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

    response = client.Reports.remove_report_scope(
        report_id=TEST_REPORT_ID,
        scopes=scopes
    )

    assert isinstance(response, Error)

