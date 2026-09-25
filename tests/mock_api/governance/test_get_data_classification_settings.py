import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import DataClassificationSettings, Error
from smartsheet.models.enums import ApproverType, AssetType, DowngradeApprovalMode
from tests.mock_api.governance.common_test_constants import TEST_ASSET_ID, TEST_PLAN_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)

TEST_ORG_ID = 1556806293055364
TEST_LABEL_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
TEST_LABEL_ID_2 = "4aa85f64-5717-4562-b3fc-2c963f66afa7"

EXPECTED_ALL_RESPONSE_PROPERTIES = {
    "orgId": TEST_ORG_ID,
    "planId": TEST_PLAN_ID,
    "isDisabled": False,
    "guidelinesUrl": "https://wiki.example.com/classification-guide",
    "allowManualChange": True,
    "labels": [
        {
            "id": TEST_LABEL_ID,
            "name": "Confidential",
            "description": "Highly sensitive information",
            "color": "#ffe0e3",
            "sensitivityOrder": 1,
            "isDefault": False,
        },
        {
            "id": TEST_LABEL_ID_2,
            "name": "Internal",
            "description": "For internal use only",
            "color": "#b9f4c3",
            "sensitivityOrder": 2,
            "isDefault": True,
        },
    ],
    # CUSTOM mode: only labelApprovers is populated, no top-level approvers.
    # WORKSPACE_ADMINS ids serialise as absent (empty TypedList is omitted by serialize()).
    "downgradeApprovalSettings": {
        "mode": DowngradeApprovalMode.CUSTOM.value,
        "labelApprovers": [
            {
                "labelId": TEST_LABEL_ID_2,
                "approvers": [
                    {"type": ApproverType.USERS.value, "ids": [5448085317937028]},
                    {"type": ApproverType.WORKSPACE_ADMINS.value},
                ],
            }
        ],
    },
}

EXPECTED_REQUIRED_RESPONSE_PROPERTIES = {
    "orgId": TEST_ORG_ID,
    "planId": TEST_PLAN_ID,
    "isDisabled": False,
    "labels": [
        {
            "id": TEST_LABEL_ID,
            "name": "Confidential",
            "color": "#ffe0e3",
            "sensitivityOrder": 1,
            "isDefault": False,
        }
    ],
    "downgradeApprovalSettings": {"mode": DowngradeApprovalMode.NONE.value},
}


def _assert_asset_query(asset_type):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    client.Governance.get_data_classification_settings(asset_type=asset_type, asset_id=TEST_ASSET_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert query == {"assetType": [asset_type.value], "assetId": [str(TEST_ASSET_ID)]}

    assert url.path == "/2.0/governance/data-classification/settings"
    assert wiremock_request["method"] == "GET"


def test_get_data_classification_settings_generated_url_is_correct():
    """Test that the URL is correctly generated for GET /governance/data-classification/settings."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    query = parse_qs(url.query)
    assert query == {"planId": [str(TEST_PLAN_ID)]}

    assert url.path == "/2.0/governance/data-classification/settings"
    assert wiremock_request["method"] == "GET"


def test_get_data_classification_settings_all_response_properties():
    """Test that all response properties are correctly deserialized (CUSTOM downgrade mode)."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert response.to_dict() == EXPECTED_ALL_RESPONSE_PROPERTIES


def test_get_data_classification_settings_required_response_properties():
    """Test that only the required response properties are deserialized (NONE downgrade mode)."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/required-response-body-properties", request_id
    )

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert response.to_dict() == EXPECTED_REQUIRED_RESPONSE_PROPERTIES


def test_get_data_classification_settings_disabled_plan():
    """Test that a disabled plan returns no labels and NONE downgrade mode."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/disabled-plan", request_id
    )

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    # serialize() omits empty TypedList, so "labels" is absent from to_dict() when the list is empty.
    assert response.to_dict() == {
        "orgId": TEST_ORG_ID,
        "planId": TEST_PLAN_ID,
        "isDisabled": True,
        "downgradeApprovalSettings": {"mode": DowngradeApprovalMode.NONE.value},
    }


def test_get_data_classification_settings_approval_needed_mode():
    """Test APPROVAL_NEEDED mode: top-level approvers list, no labelApprovers."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/downgrade-approval-mode-approval-needed",
        request_id,
    )

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert response.to_dict() == {
        "orgId": TEST_ORG_ID,
        "planId": TEST_PLAN_ID,
        "isDisabled": False,
        "allowManualChange": True,
        "labels": [
            {
                "id": TEST_LABEL_ID,
                "name": "Confidential",
                "color": "#ffe0e3",
                "sensitivityOrder": 1,
                "isDefault": False,
            }
        ],
        "downgradeApprovalSettings": {
            "mode": DowngradeApprovalMode.APPROVAL_NEEDED.value,
            "approvers": [
                {"type": ApproverType.GROUPS.value, "ids": [5129226945881988, 2877427132196740]},
                {"type": ApproverType.USERS.value, "ids": [5448085317937028]},
            ],
        },
    }


def test_get_data_classification_settings_by_sheet_generated_url_is_correct():
    """Test that assetType=sheet and assetId are sent as query params instead of planId."""
    _assert_asset_query(AssetType.SHEET)


def test_get_data_classification_settings_by_report_generated_url_is_correct():
    """Test that assetType=report and assetId are sent as query params instead of planId."""
    _assert_asset_query(AssetType.REPORT)


def test_get_data_classification_settings_by_sight_generated_url_is_correct():
    """Test that assetType=sight and assetId are sent as query params instead of planId."""
    _assert_asset_query(AssetType.SIGHT)


def test_get_data_classification_settings_by_asset_all_response_properties():
    """Test that all response properties are deserialized when resolving the plan from an asset."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    response = client.Governance.get_data_classification_settings(
        asset_type=AssetType.SHEET, asset_id=TEST_ASSET_ID
    )

    assert isinstance(response, DataClassificationSettings)

    wiremock_request = get_wiremock_request(request_id)
    assert not wiremock_request["body"]

    assert response.to_dict() == EXPECTED_ALL_RESPONSE_PROPERTIES


def test_get_data_classification_settings_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/400-response", request_id)

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, Error)


def test_get_data_classification_settings_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/500-response", request_id)

    response = client.Governance.get_data_classification_settings(plan_id=TEST_PLAN_ID)

    assert isinstance(response, Error)
