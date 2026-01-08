# pylint: disable=C0114
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

"""Shared operation builders for Smartsheet API.

This package contains shared operation builder classes that prepare API
operation dictionaries for both synchronous and asynchronous API modules.
By extracting the operation preparation logic into shared builders, we
minimize code duplication between sync and async implementations.

The operation builders handle:
- Building operation dictionaries with method, path, and parameters
- Parameter validation and transformation
- Query parameter configuration
- Request body preparation

These builders are used by both sync API modules (sheets.py, users.py, etc.)
and async API modules (async_sheets.py, async_users.py, etc.) to ensure
consistent behavior and reduce maintenance burden.

Example:
    >>> from smartsheet.operations import SheetsOperations, WorkspacesOperations
    >>>
    >>> # Build an add_rows operation
    >>> operation, expected = SheetsOperations.build_add_rows(123, rows)
    >>> print(operation["method"])
    'POST'
    >>> print(operation["path"])
    '/sheets/123/rows'
    >>>
    >>> # Build a list_workspaces operation
    >>> operation, expected = WorkspacesOperations.build_list_workspaces(
    ...     pagination_type='token',
    ...     max_items=100
    ... )
    >>> print(operation["method"])
    'GET'
"""

from .sheets_operations import SheetsOperations
from .workspaces_operations import WorkspacesOperations

__all__ = [
    'SheetsOperations',
    'WorkspacesOperations',
]
