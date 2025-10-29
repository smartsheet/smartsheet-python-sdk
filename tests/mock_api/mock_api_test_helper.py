import os
import requests
import smartsheet
from smartsheet.exceptions import ApiError


def clean_api_error(test_func):
    def wrapper(*args, **kwargs):
        try:
            test_func(*args, **kwargs)
        except ApiError as error:
            assert False, 'ApiError: ' + error.message

    return wrapper


class MockApiTestHelper(object):
    def setup_method(self, method):
        self.client = smartsheet.Smartsheet(access_token='abc123', api_base='http://localhost:8082')
        self.client.errors_as_exceptions()

    def check_error_code(self, exception_info, expected_error_code):
        actual_error_code = exception_info.value.error.result.error_code

        if self.is_test_scenario_error_code(actual_error_code):
            raise exception_info.value

        assert actual_error_code == expected_error_code

    def is_test_scenario_error_code(self, error_code):
        return error_code == 9999


def get_mock_api_client(test_name: str, request_id: str) -> smartsheet.Smartsheet:
    client = smartsheet.Smartsheet(access_token='abc123', api_base='http://localhost:8082/2.0')
    client.with_wiremock_test_case(test_name, request_id)
    return client


def get_wiremock_request(request_id: str) -> dict:
    """
    Fetch request details from WireMock admin API using the request ID.

    Args:
        request_id (str): The unique request ID to search for

    Returns:
        dict: The request details from WireMock, or None if not found

    Raises:
        requests.RequestException: If the HTTP request fails
        ValueError: If not exactly 1 match
    """
    admin_url = "http://localhost:8082/__admin/requests/find"

    # Search for requests with the specific request ID in headers
    search_criteria = {
        "headers": {
            "X-Request-Id": {
                "equalTo": request_id
            }
        }
    }

    response = requests.post(admin_url, json=search_criteria, timeout=30)
    response.raise_for_status()

    data = response.json()
    requests_found = data.get("requests", [])

    if len(requests_found) != 1:
        raise ValueError(f'Found {len(requests_found)} requests, expected 1')
    return requests_found[0]
