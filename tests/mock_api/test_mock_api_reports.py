import uuid
from urllib.parse import urlparse

from smartsheet.models import Error
from tests.mock_api.mock_api_test_helper import get_mock_api_client, get_wiremock_request

REPORT_ID = 1234567890123456


def test_delete_report_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/delete-report/all-response-body-properties", request_id
    )

    client.Reports.delete_report(REPORT_ID)

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])

    assert url.path == f'/2.0/reports/{REPORT_ID}'


def test_delete_report():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/delete-report/all-response-body-properties", request_id
    )

    response = client.Reports.delete_report(REPORT_ID)

    assert response.message == 'SUCCESS'
    assert response.result_code == 0


def test_delete_report_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Reports.delete_report(REPORT_ID)

    assert isinstance(response, Error)


def test_delete_report_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Reports.delete_report(REPORT_ID)

    assert isinstance(response, Error)
