# pylint: disable=C0302,C0111, E1121
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.



class SmartsheetException(Exception):
    """Root for SmartsheetErrors, never raised directly."""


class ApiError(SmartsheetException):
    """Errors produced by the Smartsheet API."""

    def __init__(self, error, message=None, should_retry=False):
        """
        An error produced by the API.

        Args:
            error: An instance of the Error data type.
            message (str): A human-readable message that can be
                displayed to the end user. Is None, if unavailable.
        """
        super().__init__(error)
        self.error = error
        self.message = message
        self.should_retry = should_retry

    def __repr__(self):
        return f"ApiError({self.error})"


class HttpError(SmartsheetException):
    """Errors produced at the HTTP layer."""

    def __init__(self, status_code, body):
        super().__init__(status_code, body)
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return f"HttpError({self.status_code}, {self.body!r})"


class InternalServerError(HttpError):
    """Errors due to a problem on Smartsheet."""

    def __init__(self, status_code, message):
        super().__init__(status_code, status_code, message)
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return f"InternalServerError({self.status_code}, {self.message!r})"


class UnexpectedRequestError(SmartsheetException):
    """Error originating from Requests API."""

    def __init__(self, request, response):
        super().__init__(request, response)
        self.request = request
        self.response = response

    def __repr__(self):
        return f"UnexpectedRequestError({self.request!r}, {self.response!r})"


class SystemMaintenanceError(ApiError):
    """Smartsheet.com is currently offline for system maintenance. ..."""

    def __init__(self, error, message):
        super().__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return f"SystemMaintenanceError({self.message!r})"


class ServerTimeoutExceededError(ApiError):
    """Server timeout exceeded. Request has failed."""

    def __init__(self, error, message):
        super().__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return f"ServerTimeoutExceededError({self.message!r})"


class RateLimitExceededError(ApiError):
    """Rate limit exceeded."""

    def __init__(self, error, message):
        super().__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return f"RateLimitExceededError({self.message!r})"


class UnexpectedErrorShouldRetryError(ApiError):
    """An unexpected error has occurred. Please retry your request. If ..."""

    def __init__(self, error, message):
        super().__init__(error, message, True)
        self.error = error
        self.message = message
        self.should_retry = True

    def __repr__(self):
        return f"UnexpectedErrorShouldRetryError({self.message!r})"
