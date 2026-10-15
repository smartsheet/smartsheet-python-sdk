"""Unit tests for mapping API error codes to error results in smartsheet/smartsheet.py"""

import json

import requests

from smartsheet import exceptions
from smartsheet.smartsheet import OperationErrorResult


def _error_response(status_code, body):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = json.dumps(body).encode("utf-8")  # pylint: disable=W0212
    return resp


class TestInsufficientScope:
    """Error code 4008: the access token lacks scopes the operation requires"""

    def test_maps_to_insufficient_scope_error(self):
        resp = _error_response(
            403,
            {
                "errorCode": 4008,
                "message": "The access token provided does not contain the required scopes: READ_SHEETS.",
                "refId": "abc123",
            },
        )

        result = OperationErrorResult(None, resp).native(None).result

        assert result.to_dict() == {
            "name": "InsufficientScopeError",
            "statusCode": 403,
            "code": 4008,
            "errorCode": 4008,
            "message": "The access token provided does not contain the required scopes: READ_SHEETS.",
            "refId": "abc123",
            "recommendation": "Do not retry. Re-authorize the access token with the scopes named in the error message.",
            "shouldRetry": False,
        }

    def test_raised_exception_is_a_non_retryable_api_error(self):
        resp = _error_response(403, {"errorCode": 4008, "message": "m"})
        native = OperationErrorResult(None, resp).native(None)

        # The same lookup Smartsheet.request() does when raise_exceptions is on.
        error = getattr(exceptions, native.result.name)(native, "4008: m")

        assert isinstance(error, exceptions.ApiError)
        assert error.should_retry is False
        assert repr(error) == "InsufficientScopeError('4008: m')"

    def test_not_authorized_still_maps_to_api_error(self):
        resp = _error_response(403, {"errorCode": 1004, "message": "You are not authorized to perform this action."})

        result = OperationErrorResult(None, resp).native(None).result

        assert result.name == "ApiError"
        assert result.should_retry is False
