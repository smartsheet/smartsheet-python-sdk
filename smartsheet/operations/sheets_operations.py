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

"""Shared operation builders for Sheets API.

This module provides shared operation builder functions for Sheets API operations.
These builders create operation dictionaries that can be used by both synchronous
and asynchronous API implementations, eliminating code duplication.

The operation builders are pure functions that:
- Take operation parameters as input
- Return a tuple of (operation_dict, expected_types)
- Do not perform HTTP requests or have side effects
- Handle parameter validation and transformation

Example:
    >>> from smartsheet.operations.sheets_operations import SheetsOperations
    >>> from smartsheet.types import TypedList
    >>> from smartsheet.models import Row
    >>> 
    >>> # Prepare rows
    >>> rows = TypedList(Row)
    >>> rows.append(Row({'cells': [...]}))
    >>> 
    >>> # Build operation
    >>> operation, expected = SheetsOperations.build_add_rows(123, rows)
    >>> print(operation["method"])
    'POST'
    >>> print(operation["path"])
    '/sheets/123/rows'
"""

from __future__ import absolute_import

from typing import Tuple, Dict, Any, List, Union

from ..models import Row
from ..types import TypedList
from ..util import fresh_operation


class SheetsOperations:
    """Shared operation builders for Sheets API.
    
    This class provides static methods that build operation dictionaries for
    Sheets API operations. These methods are used by both sync and async
    implementations to ensure consistent behavior.
    
    All methods are static and pure functions - they don't modify state or
    perform HTTP requests. They simply prepare operation dictionaries that
    can be passed to HTTP clients.
    """

    @staticmethod
    def build_add_rows(
        sheet_id: int,
        list_of_rows: Union[List[Row], TypedList]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Build operation for adding rows to a sheet.
        
        This method prepares the operation dictionary for inserting one or more
        rows into a sheet. It handles normalization of single row inputs into
        a list format.
        
        Args:
            sheet_id: The ID of the sheet to add rows to
            list_of_rows: A list of Row objects or a single Row object/dict.
                If a single row is provided, it will be wrapped in a TypedList.
        
        Returns:
            A tuple containing:
                - operation: Dict with method, path, json, and query_params
                - expected: List of expected response types ["Result", "Row"]
        
        Example:
            >>> from smartsheet.models import Row
            >>> from smartsheet.types import TypedList
            >>> 
            >>> rows = TypedList(Row)
            >>> rows.append(Row({'to_bottom': True, 'cells': [...]}))
            >>> 
            >>> operation, expected = SheetsOperations.build_add_rows(123, rows)
            >>> # operation can now be passed to prepare_request and request
        """
        # Normalize single row to list
        if isinstance(list_of_rows, (dict, Row)):
            arg_value = list_of_rows
            list_of_rows = TypedList(Row)
            list_of_rows.append(arg_value)

        _op = fresh_operation("add_rows")
        _op["method"] = "POST"
        _op["path"] = "/sheets/" + str(sheet_id) + "/rows"
        _op["json"] = list_of_rows

        expected = ["Result", "Row"]

        return _op, expected
