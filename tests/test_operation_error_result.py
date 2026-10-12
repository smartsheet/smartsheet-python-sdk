# pylint: disable=C0103,W0212
"""Unit tests for OperationErrorResult.native() JSON decode error handling."""

import json

import requests

from smartsheet.smartsheet import OperationErrorResult


class FakeResponse:

    def __init__(self, json_exception, status_code=500):
        self._json_exception = json_exception
        self.status_code = status_code

    def json(self):
        raise self._json_exception


class TestOperationErrorResultNative:

    def test_handles_stdlib_json_decode_error(self):
        resp = FakeResponse(json.JSONDecodeError("Expecting value", "", 0))
        result = OperationErrorResult("op_result", resp).native("Error")
        assert result.result.code == 0

    def test_handles_requests_json_decode_error(self):
        # requests raises its own JSONDecodeError instead of the stdlib
        # json one when simplejson is installed, so this must be caught too.
        resp = FakeResponse(
            requests.exceptions.JSONDecodeError("Expecting value", "", 0)
        )
        result = OperationErrorResult("op_result", resp).native("Error")
        assert result.result.code == 0

    def test_reraises_other_exceptions(self):
        resp = FakeResponse(ValueError("not a json decode error"))
        import pytest
        with pytest.raises(ValueError):
            OperationErrorResult("op_result", resp).native("Error")
