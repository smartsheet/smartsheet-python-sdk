# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
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

"""Shared operation builders for Workspaces API.

This module provides shared operation builder functions for Workspaces API operations.
These builders create operation dictionaries that can be used by both synchronous
and asynchronous API implementations, eliminating code duplication.

The operation builders are pure functions that:
- Take operation parameters as input
- Return a tuple of (operation_dict, expected_types)
- Do not perform HTTP requests or have side effects
- Handle parameter validation and transformation

Example:
    >>> from smartsheet.operations.workspaces_operations import WorkspacesOperations
    >>> 
    >>> # Build operation for listing workspaces with token pagination
    >>> operation, expected = WorkspacesOperations.build_list_workspaces(
    ...     pagination_type='token',
    ...     max_items=100
    ... )
    >>> print(operation["method"])
    'GET'
    >>> print(operation["path"])
    '/workspaces'
"""

from __future__ import absolute_import

import warnings
from typing import Tuple, Dict, Any, List, Optional

from ..util import fresh_operation


class WorkspacesOperations:
    """Shared operation builders for Workspaces API.
    
    This class provides static methods that build operation dictionaries for
    Workspaces API operations. These methods are used by both sync and async
    implementations to ensure consistent behavior.
    
    All methods are static and pure functions - they don't modify state or
    perform HTTP requests. They simply prepare operation dictionaries that
    can be passed to HTTP clients.
    """

    @staticmethod
    def build_list_workspaces(
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        include_all: Optional[bool] = None,
        last_key: Optional[str] = None,
        max_items: Optional[int] = None,
        pagination_type: Optional[str] = None
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Build operation for listing workspaces.
        
        This method prepares the operation dictionary for retrieving the list
        of workspaces the authenticated user may access. It supports both
        legacy offset-based pagination and modern token-based pagination.
        
        Args:
            page_size: [DEPRECATED] The maximum number of items to return per page.
                Use pagination_type='token' with max_items instead.
            page: [DEPRECATED] Which page to return.
                Use pagination_type='token' with last_key instead.
            include_all: [DEPRECATED] If true, include all results (i.e. do not paginate).
                Use pagination_type='token' instead.
            last_key: Pagination cursor for next page (token pagination only).
            max_items: Maximum items per page (token pagination only).
                Must be a positive integer.
            pagination_type: Use 'token' for efficient cursor-based pagination.
                Defaults to legacy offset-based pagination if not specified.
        
        Returns:
            A tuple containing:
                - operation: Dict with method, path, and query_params
                - expected: List of expected response types ["IndexResult", "Workspace"]
        
        Raises:
            ValueError: If pagination_type is not 'token' or None, or if max_items <= 0
                when using token pagination.
        
        Example:
            Token-based pagination (recommended)::
            
                >>> operation, expected = WorkspacesOperations.build_list_workspaces(
                ...     pagination_type='token',
                ...     max_items=100
                ... )
                >>> print(operation["query_params"]["paginationType"])
                'token'
            
            Legacy pagination (deprecated)::
            
                >>> operation, expected = WorkspacesOperations.build_list_workspaces(
                ...     page_size=50,
                ...     page=1
                ... )
                >>> print(operation["query_params"]["pageSize"])
                50
        """
        # Parameter validation
        if pagination_type is not None and pagination_type not in ['token']:
            raise ValueError("pagination_type must be 'token' or None")
        if pagination_type == 'token' and max_items is not None and max_items <= 0:
            raise ValueError("max_items must be a positive integer")

        _op = fresh_operation("list_workspaces")
        _op["method"] = "GET"
        _op["path"] = "/workspaces"

        # Issue deprecation warnings for old parameters when used
        if page_size is not None:
            warnings.warn(
                "page_size parameter is deprecated. Use pagination_type='token' with max_items instead.",
                DeprecationWarning,
                stacklevel=3  # Adjusted for call through sync/async wrapper
            )
        if page is not None:
            warnings.warn(
                "page parameter is deprecated. Use pagination_type='token' with last_key instead.",
                DeprecationWarning,
                stacklevel=3
            )
        if include_all is not None:
            warnings.warn(
                "include_all parameter is deprecated. Use pagination_type='token' instead.",
                DeprecationWarning,
                stacklevel=3
            )

        if pagination_type == "token":
            _op["query_params"]["lastKey"] = last_key
            _op["query_params"]["maxItems"] = max_items
            _op["query_params"]["paginationType"] = pagination_type
        else:
            _op["query_params"]["pageSize"] = page_size
            _op["query_params"]["page"] = page
            _op["query_params"]["includeAll"] = include_all

        expected = ["IndexResult", "Workspace"]

        return _op, expected
