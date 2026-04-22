# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
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

from __future__ import absolute_import

from typing import Optional, Union

from ..types import EnumeratedValue, String, Boolean, json
from ..util import deserialize, serialize
from .enums import ColumnType, SystemColumnType


class ReportColumnIdentifier:
    """Smartsheet ReportColumnIdentifier data model.

    Object used to match a sheet column for a report. Either 'type' or 'primary' must be
    specified.

    **Column Matching Options:**
    - **Regular columns**: Specify 'type' to match columns by type (optionally with 'title'
      for additional matching).
    - **System columns**: Specify both 'type' and 'systemColumnType' to match system columns
      (e.g., Created By, Modified Date).
    - **Sheet name column**: Specify 'type=TEXT_NUMBER' and 'sheetNameColumn=True' to match
      the special "Sheet Name" column.
    - **Primary column**: Specify 'primary=True' to match the primary column. When matching
      primary columns, 'title' can be used to customize the primary column name in the
      rendered report.

    **Note:** Columns in the report are matched by the combination of 'title' and 'type'
    (and 'systemColumnType' or 'sheetNameColumn' if specified).

    **Note:** 'symbol' is not used for matching and as a result 'CHECKBOX' or 'PICKLIST'
    columns with different symbols (from different sheets) can be combined into the same
    column in the report. You cannot combine 'CHECKBOX' with 'PICKLIST' into the same column
    in the report because they are different types.
    """

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportColumnIdentifier model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._title = String()
        self._type = EnumeratedValue(ColumnType)
        self._system_column_type = EnumeratedValue(SystemColumnType)
        self._primary = Boolean()
        self._sheet_name_column = Boolean()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def title(self) -> Optional[str]:
        return self._title.value

    @title.setter
    def title(self, value: str) -> None:
        self._title.value = value

    @property
    def type(self) -> EnumeratedValue:
        return self._type

    @type.setter
    def type(self, value: Union[ColumnType, str]) -> None:
        self._type.set(value)

    @property
    def system_column_type(self) -> EnumeratedValue:
        return self._system_column_type

    @system_column_type.setter
    def system_column_type(self, value: Union[SystemColumnType, str]) -> None:
        self._system_column_type.set(value)

    @property
    def primary(self) -> Optional[bool]:
        return self._primary.value

    @primary.setter
    def primary(self, value: bool) -> None:
        self._primary.value = value

    @property
    def sheet_name_column(self) -> Optional[bool]:
        return self._sheet_name_column.value

    @sheet_name_column.setter
    def sheet_name_column(self, value: bool) -> None:
        self._sheet_name_column.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
