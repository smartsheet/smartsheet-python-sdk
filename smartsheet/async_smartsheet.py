# pylint: disable=C0103,C0111,R0902,R0913,W0614,C0302,W0401,R0912,W0611,C0301,W0621,W0404,R1720,W0702,W0613
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

"""Async client for Smartsheet API.

This module provides an async version of the Smartsheet client that uses
httpx.AsyncClient for non-blocking HTTP operations. It mirrors the synchronous
client API but uses async/await patterns.

Example:
    Basic usage with context manager::

        import asyncio
        from smartsheet import AsyncSmartsheet

        async def main():
            async with AsyncSmartsheet(access_token="your_token") as client:
                workspaces = await client.Workspaces.list_workspaces()
                print(f"Found {len(workspaces.data)} workspaces")

        asyncio.run(main())

    Manual lifecycle management::

        async def main():
            client = AsyncSmartsheet(access_token="your_token")
            try:
                workspaces = await client.Workspaces.list_workspaces()
                print(f"Found {len(workspaces.data)} workspaces")
            finally:
                await client.aclose()

        asyncio.run(main())
"""

from __future__ import absolute_import, annotations

import asyncio
import importlib
import inspect
import json
import logging
import logging.config
import os
import random
import re
import sys
import time
from typing import Optional

import httpx
import six

from . import __api_base__, __version__, models
from .async_session import async_pinned_session
from .exceptions import ApiError, HttpError, UnexpectedRequestError
from .models import Error, ErrorResult
from .util import is_multipart, serialize

__all__ = ("AsyncSmartsheet", "AsyncAbstractUserCalcBackoff")


class AsyncAbstractUserCalcBackoff:
    """Abstract base class for async backoff calculation."""
    
    async def calc_backoff(self, previous_attempts, total_elapsed_time, error_result):
        """Calculate backoff time for retry attempts.
        
        Args:
            previous_attempts (int): Number of previous retry attempts
            total_elapsed_time (float): Total elapsed time in seconds
            error_result (ErrorResult): Error result from previous attempt
            
        Returns:
            float: Backoff time in seconds (negative to stop retrying)
        """
        raise NotImplementedError(
            f"Class {self.__class__.__name__} doesn't implement calc_backoff()"
        )


class AsyncDefaultCalcBackoff(AsyncAbstractUserCalcBackoff):
    """Default async backoff calculator."""
    
    def __init__(self, max_retry_time):
        self._max_retry_time = max_retry_time

    async def calc_backoff(self, previous_attempts, total_elapsed_time, error_result):
        """Default back off calculator on retry.

        Args:
            previous_attempts (int): Number of previous retry attempts
            total_elapsed_time (float): Elapsed time in seconds
            error_result (ErrorResult): ErrorResult object for previous API attempt

        Returns:
            float: Back off time in seconds (any negative number will drop out of retry loop)
        """
        # Use exponential backoff
        backoff = (2**previous_attempts) + random.random()

        if (total_elapsed_time + backoff) > self._max_retry_time:
            return -1

        return backoff


class AsyncSmartsheet:
    """Async client for making requests to the Smartsheet API.
    
    This class provides an async interface to the Smartsheet API using httpx.AsyncClient
    for non-blocking HTTP operations. It mirrors the synchronous Smartsheet client API
    but uses async/await patterns throughout.
    
    The client should be used as an async context manager to ensure proper resource
    cleanup, or you must manually call aclose() when done.
    
    Attributes:
        Sheets: Async Sheets API operations
        Workspaces: Async Workspaces API operations
        models: Reference to smartsheet.models module
        raise_exceptions: Whether to raise exceptions on API errors (default: False)
    
    Example:
        >>> async with AsyncSmartsheet(access_token="token") as client:
        ...     result = await client.Sheets.add_rows(sheet_id, rows)
        ...     print(f"Added {len(result.data)} rows")
    """

    models = models

    def __init__(
        self,
        access_token: Optional[str] = None,
        max_connections: int = 8,
        user_agent: Optional[str] = None,
        max_retry_time: int = 30,
        proxies: Optional[dict] = None,
        api_base: str = __api_base__,
    ):
        """Initialize async Smartsheet client.

        Args:
            access_token: Access Token for making client requests. May also be set
                as an env variable in SMARTSHEET_ACCESS_TOKEN. (required)
            max_connections: Maximum connection pool size.
            max_retry_time: User provided maximum elapsed time for retry attempts.
            user_agent: The user agent to use when making requests. This helps us
                identify requests coming from your application. We recommend you use
                the format "AppName/Version". If set, we append
                "/SmartsheetPythonSDK/__version__" to the user_agent.
            proxies: Proxy configuration dict. See httpx documentation for details.
            api_base: Base URL for API requests (default: https://api.smartsheet.com/2.0)
        
        Raises:
            ValueError: If access_token is not provided and not set in environment
        """
        self.raise_exceptions = False
        
        if access_token:
            self._access_token = access_token
        else:
            self._access_token = os.environ.get("SMARTSHEET_ACCESS_TOKEN", None)

        if self._access_token is None:
            raise ValueError(
                "Access Token must be set in the environment "
                "or passed to smartsheet.AsyncSmartsheet() "
                "as a parameter."
            )

        if isinstance(max_retry_time, AsyncAbstractUserCalcBackoff):
            self._user_calc_backoff = max_retry_time
        else:
            self._user_calc_backoff = AsyncDefaultCalcBackoff(max_retry_time)

        self._session: Optional[httpx.AsyncClient] = None
        self._max_connections = max_connections
        self._proxies = proxies

        base_user_agent = "SmartsheetPythonSDK/" + __version__
        if user_agent:
            self._user_agent = f"{base_user_agent}/{user_agent}"
        else:
            caller = "__unknown__"
            stack = inspect.stack()
            module = inspect.getmodule(stack[-1][0])
            if module is not None:
                caller = inspect.getmodule(stack[-1][0]).__name__
            self._user_agent = f"{base_user_agent}/{caller}"

        self._log = logging.getLogger(__name__)
        self._url = ""
        self._api_base = api_base
        self._assume_user = None
        self._test_scenario_name = None
        self._wiremock_test_name = None
        self._wiremock_request_id = None
        self._change_agent = None
        self._api_modules_cache = {}

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.aclose()
        return False

    async def _ensure_session(self):
        """Ensure HTTP session is initialized."""
        if self._session is None:
            self._session = async_pinned_session(pool_maxsize=self._max_connections)
            if self._proxies:
                # httpx uses 'proxies' parameter differently than requests
                # We'll need to recreate the client with proxies
                await self._session.aclose()
                self._session = httpx.AsyncClient(
                    proxies=self._proxies,
                    limits=httpx.Limits(
                        max_connections=self._max_connections,
                        max_keepalive_connections=self._max_connections // 2
                    )
                )

    async def aclose(self):
        """Close the async HTTP session and release resources.
        
        This method should be called when you're done using the client if you're
        not using it as an async context manager.
        
        Example:
            >>> client = AsyncSmartsheet(access_token="token")
            >>> try:
            ...     result = await client.Sheets.add_rows(sheet_id, rows)
            ... finally:
            ...     await client.aclose()
        """
        if self._session is not None:
            await self._session.aclose()
            self._session = None

    def assume_user(self, email: Optional[str] = None):
        """Assume identity of specified user.

        As an administrator, you can assume the identity of any user
        in your organization.

        Args:
            email: Valid email address of user whose identity should be assumed.
                Pass None to clear the assumed user.
        """
        if email is None:
            self._assume_user = None
        else:
            self._assume_user = six.moves.urllib.parse.quote(email)

    def errors_as_exceptions(self, preference: bool = True):
        """Set preference on whether or not to raise exceptions on API errors.
        
        When preference is True, exceptions will be raised. When False,
        instances of the Error data type will be returned.

        The property `raise_exceptions` defaults to False. Therefore, this
        method should only be called if exceptions *should* be raised.

        Args:
            preference: Flag indicating whether errors should be raised as exceptions.
        """
        self.raise_exceptions = preference

    def as_test_scenario(self, name: str):
        """Identify requests made with this client as a test scenario.

        Args:
            name: The name of the test scenario.
        """
        self._test_scenario_name = name

    def with_wiremock_test_case(self, test_name: str, request_id: str):
        """Configure client with x-test-name and x-request-id headers.
        
        Used for wiremock test cases.

        Args:
            test_name: The name of the wiremock test case.
            request_id: The unique request ID for this test scenario.
        """
        self._wiremock_test_name = test_name
        self._wiremock_request_id = request_id

    def with_change_agent(self, change_agent: str):
        """Request headers will contain the 'Smartsheet-Change-Agent' header value.

        Args:
            change_agent: The name of this change agent
        """
        self._change_agent = change_agent

    async def request(self, prepped_request, expected, operation):
        """Make a request from the Smartsheet API.

        Make a request from the Smartsheet API and validate that inputs
        and outputs are as expected. The API response is converted from
        raw wire messages to a native objects based on the value of `expected`.

        Args:
            prepped_request: Prepared httpx.Request for the operation.
            expected: The expected response data type.
            operation: Dictionary containing operation details

        Returns:
            The API operation result object.
        """
        res = await self.request_with_retry(prepped_request, operation)
        native = res.native(expected)

        if not self.raise_exceptions:
            return native

        if isinstance(native, self.models.Error):
            the_ex = getattr(sys.modules[__name__], native.result.name)
            raise the_ex(native, str(native.result.code) + ": " + native.result.message)
        else:
            return native

    def _log_request(self, operation, response):
        """Wrapper for request/response logger.

        Args:
            operation: Operation dictionary
            response: httpx.Response object
        """
        # request
        self._log.info(
            '{"request": {"command": "%s %s"}}',
            response.request.method,
            response.request.url,
        )
        if response.request.content is not None:
            body_dumps = f'"<< {response.request.headers.get("Content-Type")} content type suppressed >>"'
            if response.request.headers.get("Content-Type") is not None and "application/json" in response.request.headers.get("Content-Type"):
                body = response.request.content.decode("utf8")
                body_dumps = json.dumps(json.loads(body), sort_keys=True)
            self._log.debug('{"requestBody": %s}', body_dumps)
        
        # response
        content_dumps = f'"<< {response.headers.get("Content-Type")} content type suppressed >>"'
        if response.headers.get("Content-Type") is not None and "application/json" in response.headers.get("Content-Type"):
            content = response.content.decode("utf8")
            content_dumps = json.dumps(json.loads(content), sort_keys=True)
        
        if 200 <= response.status_code <= 299:
            if operation["dl_path"] is None:
                self._log.debug(
                    '{"response": {"statusCode": %d, "reason": "%s", "content": %s}}',
                    response.status_code,
                    response.reason_phrase,
                    content_dumps,
                )
            else:
                self._log.debug(
                    '{"response": {"statusCode": %d, "reason": "%s"}}',
                    response.status_code,
                    response.reason_phrase,
                )
        else:
            self._log.error(
                '{"response": {"statusCode": %d, "reason": "%s", "content": %s}}',
                response.status_code,
                response.reason_phrase,
                content_dumps,
            )

    async def _request(self, prepped_request, operation):
        """Wrapper for the low-level Request action.

        Only low-level error handling.

        Args:
            prepped_request: Prepared httpx.Request for the operation.
            operation: Operation dictionary

        Returns:
            Operation Result object.
        """
        await self._ensure_session()
        
        try:
            res = await self._session.send(prepped_request)
            self._log_request(operation, res)
        except httpx.HTTPError as rex:
            raise UnexpectedRequestError(prepped_request, None) from rex

        if 200 <= res.status_code <= 299:
            return AsyncOperationResult(res.text, res, self, operation)
        else:
            return AsyncOperationErrorResult(res.text, res)

    async def request_with_retry(self, prepped_request, operation):
        """Perform the request with retry.

        Args:
            prepped_request: A prepared httpx.Request object for the operation.
            operation: Dictionary containing operation details

        Returns:
            Operation Result object.
        """
        attempt = 0
        start_time = time.time()
        # Make a copy of the request as the access token will be redacted on response prior to logging
        pre_redact_request = prepped_request
        
        while True:
            result = await self._request(prepped_request, operation)
            if isinstance(result, AsyncOperationErrorResult):
                native = result.native("Error")
                if native.result.should_retry:
                    attempt += 1
                    elapsed_time = time.time() - start_time
                    backoff = await self._user_calc_backoff.calc_backoff(
                        attempt, elapsed_time, native.result
                    )
                    if backoff < 0:
                        break
                    self._log.info(
                        "HttpError status_code=%s: Retrying in %.1f seconds",
                        native.result.status_code,
                        backoff,
                    )
                    await asyncio.sleep(backoff)
                    # restore un-redacted request prior to retry
                    prepped_request = pre_redact_request
                else:
                    break
            else:
                break
        return result

    def prepare_request(self, _op):
        """Generate a prepared httpx.Request object."""
        if _op["header_params"]:
            _op["headers"].update(_op["header_params"])

        if _op["path_params"]:
            for key, val in six.iteritems(_op["path_params"]):
                _op["path"] = _op["path"].replace("{" + key + "}", str(val))

        if _op["json"]:
            _op["json"] = serialize(_op["json"])

        if _op["query_params"]:
            for key, val in six.iteritems(_op["query_params"]):
                if isinstance(val, list):
                    val = ",".join([str(num) for num in val])
                _op["query_params"][key] = val

        # Build request
        req = httpx.Request(
            _op["method"],
            self._api_base + _op["path"],
            headers=_op["headers"],
            params=_op["query_params"],
            json=_op["json"] if _op["json"] else None,
            data=_op["form_data"] if _op["form_data"] else None,
        )

        req.headers.update({"User-Agent": self._user_agent})
        if _op["auth_settings"] is not None:
            auth_header_val = "Bearer " + self._access_token
            req.headers.update({"Authorization": auth_header_val})

        if self._assume_user is not None:
            req.headers.update({"Assume-User": self._assume_user})
        else:
            req.headers.pop("Assume-User", None)

        if self._test_scenario_name is not None:
            req.headers.update({"Api-Scenario": self._test_scenario_name})
        else:
            req.headers.pop("Api-Scenario", None)
            
        if self._wiremock_test_name is not None and self._wiremock_request_id is not None:
            req.headers["X-Test-Name"] = self._wiremock_test_name
            req.headers["X-Request-ID"] = self._wiremock_request_id

        if self._change_agent is not None:
            req.headers.update({"Smartsheet-Change-Agent": self._change_agent})
        else:
            req.headers.pop("Smartsheet-Change-Agent", None)

        return req

    def __getattr__(self, name):
        """Handle sub-class instantiation.

        Args:
            name: Name of smartsheet resource class to instantiate.

        Returns:
            Instance of named class.
        """
        # Check if module is already cached
        if name in self._api_modules_cache:
            return self._api_modules_cache[name]

        try:
            # Try async API class first
            class_ = getattr(
                importlib.import_module(__package__ + ".async_" + name.lower()), "Async" + name
            )
            instance = class_(self)
            # Cache the instance
            self._api_modules_cache[name] = instance
            return instance
        except (ImportError, AttributeError):
            self._log.error(
                "ImportError! Could not load async api class %s", name
            )
            raise AttributeError(f"AsyncSmartsheet has no attribute '{name}'")


class AsyncOperationResult:
    """The successful result of a call to an async operation."""

    def __init__(self, op_result, resp=None, base_obj=None, operation=None):
        """Initialize AsyncOperationResult.

        Args:
            op_result: The result of an operation not including the binary
                payload portion, if one exists. Must be a JSON string.
            resp: A raw httpx.Response object.
            base_obj: Configured core object for subsequent convenience
                method requests.
            operation: Operation dictionary
        """
        assert isinstance(
            op_result, str
        ), f"op_result: expected string, got {type(op_result)!r}"
        if resp is not None:
            assert isinstance(
                resp, httpx.Response
            ), f"resp: expected httpx.Response, got {type(resp)!r}"
        self._base = base_obj
        self.op_result = op_result
        self.resp = resp
        self.dynamic_data_types = []
        self.operation = operation

    def native(self, expected):
        """Initialize expected result object and return it.

        Args:
            expected: Expected objects to return.

        Returns:
            Operation Result object or Operation Error Result object.
        """
        try:
            data = self.resp.json()
        except ValueError:
            return AsyncOperationErrorResult(self.op_result, self.resp)

        if isinstance(expected, list):
            klass = expected[0]
            dynamic_type = expected[1]
            class_ = getattr(importlib.import_module("smartsheet.models"), klass)
            obj = class_(data, dynamic_type, self._base)
            if hasattr(obj, "request_response"):
                obj.request_response = self.resp

            return obj

        class_ = getattr(importlib.import_module("smartsheet.models"), expected)

        obj = class_(data, self._base)
        if hasattr(obj, "request_response"):
            obj.request_response = self.resp

        return obj


class AsyncOperationErrorResult:
    """The error result of a call to an async operation."""

    error_lookup = {
        0: {
            "name": "ApiError",
            "recommendation": "Do not retry without fixing the problem. ",
            "should_retry": False,
        },
        4001: {
            "name": "SystemMaintenanceError",
            "recommendation": (
                "Retry using exponential backoff. Hint: "
                "Wait time between retries should measure "
                "in minutes (not seconds)."
            ),
            "should_retry": True,
        },
        4002: {
            "name": "ServerTimeoutExceededError",
            "recommendation": "Retry using exponential backoff.",
            "should_retry": True,
        },
        4003: {
            "name": "RateLimitExceededError",
            "recommendation": (
                "Retry using exponential backoff. Hint: "
                "Reduce the rate at which you are sending "
                "requests."
            ),
            "should_retry": True,
        },
        4004: {
            "name": "UnexpectedErrorShouldRetryError",
            "recommendation": "Retry using exponential backoff.",
            "should_retry": True,
        },
    }

    def __init__(self, op_result, resp):
        """Initialize AsyncOperationErrorResult.

        Args:
            op_result: The result of an operation not including the
                binary payload portion, if one exists.
            resp: A raw httpx.Response object.
        """
        self.op_result = op_result
        self.resp = resp
        self._log = logging.getLogger(__name__)

    def native(self, expected):
        """Sadly, we won't be returning what was expected.

        Args:
            expected: Dashed expectations
        """
        # look up name of the error
        error_payload = {}
        try:
            error_payload = self.resp.json()
        except json.JSONDecodeError:
            # Do not fail if the response is not JSON
            pass
        error_code = error_payload.get("errorCode", 0)
        try:
            error_name = AsyncOperationErrorResult.error_lookup[error_code]["name"]
            recommendation = AsyncOperationErrorResult.error_lookup[error_code][
                "recommendation"
            ]
            should_retry = AsyncOperationErrorResult.error_lookup[error_code]["should_retry"]
        except:
            # If error_code is present in the response but not in the lookup, default to ApiError
            error_name = AsyncOperationErrorResult.error_lookup[0]["name"]
            recommendation = AsyncOperationErrorResult.error_lookup[0]["recommendation"]
            should_retry = AsyncOperationErrorResult.error_lookup[0]["should_retry"]

        obj = Error(
            {
                "result": ErrorResult(
                    {
                        "name": error_name,
                        "status_code": self.resp.status_code,
                        "code": error_code,
                        "message": error_payload.get("message"),
                        "ref_id": error_payload.get("refId"),
                        "recommendation": recommendation,
                        "should_retry": should_retry,
                    }
                ),
                "request_response": self.resp,
            }
        )
        return obj
