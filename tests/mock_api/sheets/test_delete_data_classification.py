import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from tests.mock_api.sheets.common_test_constants import TEST_SHEET_ID, TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_delete_data_classification_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/delete-data-classification/all-response-body-properties", request_id
    )

    client.Sheets.delete_data_classification(
        sheet_id=TEST_SHEET_ID,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/sheets/{TEST_SHEET_ID}/dataclassification'


def test_delete_data_classification_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sheets/delete-data-classification/all-response-body-properties", request_id
    )

    response = client.Sheets.delete_data_classification(
        sheet_id=TEST_SHEET_ID,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE


def test_delete_data_classification_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sheets.delete_data_classification(
        sheet_id=TEST_SHEET_ID,
    )

    assert isinstance(response, Error)


def test_delete_data_classification_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sheets.delete_data_classification(
        sheet_id=TEST_SHEET_ID,
    )

    assert isinstance(response, Error)
