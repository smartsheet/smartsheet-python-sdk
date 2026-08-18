import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error
from smartsheet.models.data_classification_settings import DataClassificationSettings
from tests.mock_api.governance.common_test_constants import TEST_PLAN_ID
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_get_data_classification_settings_url():
    """Correct URL and query param are sent."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    client.Governance.get_data_classification_settings(TEST_PLAN_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    assert url.path == "/2.0/governance/data-classification/settings"
    assert wiremock_request["method"] == "GET"
    assert parse_qs(url.query) == {"planId": [str(TEST_PLAN_ID)]}


def test_get_data_classification_settings_all_response_body_properties():
    """All optional fields and CUSTOM-mode downgrade settings are deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/all-response-body-properties", request_id
    )

    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)
    assert not get_wiremock_request(request_id)["body"]

    assert response.to_dict() == {
        "orgId": 1244212,
        "planId": 41878788,
        "isDisabled": False,
        "guidelinesUrl": "https://wiki.example.com/classification-guide",
        "allowManualChange": True,
        "labels": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Confidential",
                "description": "Highly sensitive information",
                "color": "#FFE0E3",
                "sensitivityOrder": 1,
                "isDefault": False,
            },
            {
                "id": "4aa85f64-5717-4562-b3fc-2c963f66afa7",
                "name": "Internal",
                "description": "For internal use only",
                "color": "#E0F0FF",
                "sensitivityOrder": 2,
                "isDefault": True,
            },
        ],
        # CUSTOM mode: only labelApprovers is populated, no top-level approvers.
        # WORKSPACE_ADMINS ids serialise as absent (empty TypedList is omitted by serialize()).
        "downgradeApprovalSettings": {
            "mode": "CUSTOM",
            "labelApprovers": [
                {
                    "labelId": "4aa85f64-5717-4562-b3fc-2c963f66afa7",
                    "approvers": [
                        {"type": "USERS", "ids": [7001]},
                        {"type": "WORKSPACE_ADMINS"},
                    ],
                }
            ],
        },
    }


def test_get_data_classification_settings_required_response_body_properties():
    """Minimum required fields with NONE downgrade mode."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/required-response-body-properties", request_id
    )

    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)
    assert response.to_dict() == {
        "orgId": 1244212,
        "planId": 41878788,
        "isDisabled": False,
        "labels": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Confidential",
                "color": "#FFE0E3",
                "sensitivityOrder": 1,
                "isDefault": False,
            }
        ],
        "downgradeApprovalSettings": {"mode": "NONE"},
    }


def test_get_data_classification_settings_disabled_plan():
    """When classification is disabled, labels is empty and downgrade settings are NONE."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/disabled-plan", request_id
    )

    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)
    # serialize() omits empty TypedList, so "labels" is absent from to_dict() when the list is empty.
    assert response.to_dict() == {
        "orgId": 1244212,
        "planId": 41878788,
        "isDisabled": True,
        "downgradeApprovalSettings": {"mode": "NONE"},
    }


def test_get_data_classification_settings_approval_needed_mode():
    """APPROVAL_NEEDED mode: top-level approvers list, no labelApprovers."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/governance/get-data-classification-settings/downgrade-approval-mode-approval-needed",
        request_id,
    )

    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)

    assert isinstance(response, DataClassificationSettings)
    assert response.to_dict() == {
        "orgId": 1244212,
        "planId": 41878788,
        "isDisabled": False,
        "allowManualChange": True,
        "labels": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Confidential",
                "color": "#FFE0E3",
                "sensitivityOrder": 1,
                "isDefault": False,
            }
        ],
        "downgradeApprovalSettings": {
            "mode": "APPROVAL_NEEDED",
            "approvers": [
                {"type": "GROUPS", "ids": [5001, 5002]},
                {"type": "USERS", "ids": [7001]},
            ],
        },
    }


def test_get_data_classification_settings_error_400():
    """400 response is returned as Error."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/400-response", request_id)
    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)
    assert isinstance(response, Error)


def test_get_data_classification_settings_error_403():
    """403 response is returned as Error (caller not authorized for this plan)."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/403-response", request_id)
    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)
    assert isinstance(response, Error)


def test_get_data_classification_settings_error_500():
    """500 response is returned as Error."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client("/errors/500-response", request_id)
    response = client.Governance.get_data_classification_settings(TEST_PLAN_ID)
    assert isinstance(response, Error)
