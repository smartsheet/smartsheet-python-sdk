# pylint: disable=C0111,R0902,R0913,C0301,R0914
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

"""Async Sheets API operations.

This module provides async versions of Sheets API operations using async/await
patterns. Currently implements a proof-of-concept with the add_rows method.

Example:
    Adding rows to a sheet asynchronously::

        import asyncio
        from smartsheet import AsyncSmartsheet
        from smartsheet.models import Row, Cell

        async def main():
            async with AsyncSmartsheet(access_token="token") as client:
                # Create rows to add
                row1 = Row()
                row1.to_bottom = True
                row1.cells = [
                    Cell({'column_id': 123, 'value': 'New Value 1'}),
                    Cell({'column_id': 456, 'value': 'New Value 2'})
                ]
                
                # Add rows asynchronously
                result = await client.Sheets.add_rows(sheet_id, [row1])
                print(f"Added {len(result.data)} rows")

        asyncio.run(main())
"""

from __future__ import absolute_import

import logging
from typing import Union, List

from .models import Error, Result, Row
from .types import TypedList
from .util import fresh_operation
from .operations.sheets_operations import SheetsOperations


class AsyncSheets:
    """Async class for handling Sheets operations.
    
    This class provides async methods for interacting with the Smartsheet Sheets API.
    Currently implements a proof-of-concept with the add_rows method. Additional
    methods will be added in future iterations.
    
    Attributes:
        _base: Reference to the parent AsyncSmartsheet client
        _log: Logger instance for this class
    """

    def __init__(self, smartsheet_obj):
        """Init AsyncSheets with base AsyncSmartsheet object.
        
        Args:
            smartsheet_obj: The parent AsyncSmartsheet client instance
        """
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    async def add_rows(self, sheet_id: int, list_of_rows) -> Union[Result[Union[Row, List[Row]]], Error]:
        """Insert one or more Rows into the specified Sheet asynchronously.

        If multiple rows are specified in the request, all rows
        must be inserted at the same location (i.e. the **toTop**,
        **toBottom**, **parentId**, **siblingId**, and **above** attributes
        must be the same for all rows in the request.)

        In a parent row, values of the following fields will be
        auto-calculated based upon values in the child rows (and therefore
        cannot be updated using the API): Start Date, End Date, Duration, %
        Complete.

        Args:
            sheet_id: Sheet ID
            list_of_rows: An array of Row objects with the following attributes:

               One or more location-specifier attributes (optional)

               format (optional)

               expanded (optional)

               locked (optional)

               A cells attribute set to an array of Cell objects.
               To insert an empty row, set the cells attribute to empty or null.
               Each Cell object may contain the following attributes:

                   columnId (required)

                   value (required)

                   strict (optional)

                   format (optional)

                   hyperlink (optional)

        Returns:
            Union[Result[Union[Row, List[Row]]], Error]: The result of the operation -
                either a list or a single object, or an Error object if the request fails.
        
        Example:
            >>> async with AsyncSmartsheet(access_token="token") as client:
            ...     row = Row()
            ...     row.to_bottom = True
            ...     row.cells = [Cell({'column_id': 123, 'value': 'Test'})]
            ...     result = await client.Sheets.add_rows(sheet_id, [row])
            ...     print(f"Added {len(result.data)} rows")
        """
        _op, expected = SheetsOperations.build_add_rows(sheet_id, list_of_rows)

        prepped_request = self._base.prepare_request(_op)
        response = await self._base.request(prepped_request, expected, _op)

        return response
