import json
import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from smartsheet.models.data_classification import DataClassification
from tests.mock_api.sheets.common_test_constants import TEST_SHEET_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_set_data_classification_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/set-data-classification/all-response-body-properties", request_id
    )

    data_classification_obj = DataClassification({"dataClassification": "CONFIDENTIAL"})

    client.Sheets.set_data_classification(
        sheet_id=TEST_SHEET_ID,
        data_classification_obj=data_classification_obj,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/sheets/{TEST_SHEET_ID}/dataclassification'


def test_set_data_classification_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/set-data-classification/all-response-body-properties", request_id
    )

    data_classification_obj = DataClassification({"dataClassification": "CONFIDENTIAL"})

    response = client.Sheets.set_data_classification(
        sheet_id=TEST_SHEET_ID,
        data_classification_obj=data_classification_obj,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {"dataClassification": "CONFIDENTIAL"}


def test_set_data_classification_custom_label():
    """dataClassification is a free-form string set by plan admins in Admin
    Center, not a fixed enum, so a non-canonical, custom label must be
    accepted without raising an error."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/set-data-classification/all-response-body-properties", request_id
    )

    data_classification_obj = DataClassification({"dataClassification": "Top Secret"})

    response = client.Sheets.set_data_classification(
        sheet_id=TEST_SHEET_ID,
        data_classification_obj=data_classification_obj,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {"dataClassification": "Top Secret"}


def test_set_data_classification_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    data_classification_obj = DataClassification({"dataClassification": "CONFIDENTIAL"})

    response = client.Sheets.set_data_classification(
        sheet_id=TEST_SHEET_ID,
        data_classification_obj=data_classification_obj,
    )

    assert isinstance(response, Error)


def test_set_data_classification_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    data_classification_obj = DataClassification({"dataClassification": "CONFIDENTIAL"})

    response = client.Sheets.set_data_classification(
        sheet_id=TEST_SHEET_ID,
        data_classification_obj=data_classification_obj,
    )

    assert isinstance(response, Error)
