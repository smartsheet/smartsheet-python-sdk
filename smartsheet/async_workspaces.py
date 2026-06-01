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

"""Async Workspaces API operations.

This module provides async versions of Workspaces API operations using async/await
patterns. Currently implements a proof-of-concept with the list_workspaces method.

Example:
    Listing workspaces asynchronously::

        import asyncio
        from smartsheet import AsyncSmartsheet

        async def main():
            async with AsyncSmartsheet(access_token="token") as client:
                # List workspaces with token pagination
                result = await client.Workspaces.list_workspaces(
                    pagination_type='token',
                    max_items=100
                )
                
                print(f"Found {len(result.data)} workspaces")
                for workspace in result.data:
                    print(f"  - {workspace.name}")
                
                # Check if there are more results
                if hasattr(result, 'next_token') and result.next_token:
                    print(f"More results available, next_token: {result.next_token}")

        asyncio.run(main())
"""

from __future__ import absolute_import

import logging
import warnings
from typing import Union, Optional

from .models import Error, IndexResult, Workspace
from .util import fresh_operation
from .operations.workspaces_operations import WorkspacesOperations


class AsyncWorkspaces:
    """Async class for handling Workspaces operations.
    
    This class provides async methods for interacting with the Smartsheet Workspaces API.
    Currently implements a proof-of-concept with the list_workspaces method. Additional
    methods will be added in future iterations.
    
    Attributes:
        _base: Reference to the parent AsyncSmartsheet client
        _log: Logger instance for this class
    """

    def __init__(self, smartsheet_obj):
        """Init AsyncWorkspaces with base AsyncSmartsheet object.
        
        Args:
            smartsheet_obj: The parent AsyncSmartsheet client instance
        """
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    async def list_workspaces(
        self,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        include_all: Optional[bool] = None,
        last_key: Optional[str] = None,
        max_items: Optional[int] = None,
        pagination_type: Optional[str] = None
    ) -> Union[IndexResult[Workspace], Error]:
        """Get the list of Workspaces the authenticated User may access asynchronously.

        Args:
            page_size: [DEPRECATED] The maximum number of items to
                return per page. Use pagination_type='token' with max_items instead.
            page: [DEPRECATED] Which page to return.
                Use pagination_type='token' with last_key instead.
            include_all: [DEPRECATED] If true, include all results
                (i.e. do not paginate). Use pagination_type='token' instead.
            last_key: Pagination cursor for next page (token pagination only).
            max_items: Maximum items per page (token pagination only).
                Must be a positive integer.
            pagination_type: Use 'token' for efficient cursor-based pagination.
                Defaults to legacy offset-based pagination if not specified.

        Returns:
            Union[IndexResult[Workspace], Error]: The result of the operation, or an
                Error object if the request fails. When using legacy pagination, contains
                paginated results with total_count, total_pages, etc.

        Raises:
            ValueError: If pagination_type is not 'token' or None, or if max_items <= 0
                when using token pagination.
        
        Example:
            Using token-based pagination (recommended)::
            
                >>> async with AsyncSmartsheet(access_token="token") as client:
                ...     result = await client.Workspaces.list_workspaces(
                ...         pagination_type='token',
                ...         max_items=100
                ...     )
                ...     print(f"Found {len(result.data)} workspaces")
                ...
                ...     # Get next page if available
                ...     if hasattr(result, 'next_token') and result.next_token:
                ...         next_result = await client.Workspaces.list_workspaces(
                ...             pagination_type='token',
                ...             last_key=result.next_token,
                ...             max_items=100
                ...         )
            
            Using legacy pagination (deprecated)::
            
                >>> async with AsyncSmartsheet(access_token="token") as client:
                ...     result = await client.Workspaces.list_workspaces(
                ...         page_size=50,
                ...         page=1
                ...     )
                ...     print(f"Found {len(result.data)} workspaces")
        """
        _op, expected = WorkspacesOperations.build_list_workspaces(
            page_size=page_size,
            page=page,
            include_all=include_all,
            last_key=last_key,
            max_items=max_items,
            pagination_type=pagination_type
        )

        prepped_request = self._base.prepare_request(_op)
        response = await self._base.request(prepped_request, expected, _op)

        return response
