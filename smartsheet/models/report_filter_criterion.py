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

from typing import List, Optional, Union

from ..types import EnumeratedValue, TypedObject, json
from ..util import deserialize, serialize
from .enums import ReportFilterOperator
from .report_column_identifier import ReportColumnIdentifier


class ReportFilterCriterion:
    """Smartsheet ReportFilterCriterion data model.

    Criteria object specifying custom criteria against which to match cell values.

    The values property can contain:
    - Simple values: strings, numbers, or None
    - Object values: dicts with 'objectType' (DATE or CURRENT_USER) and 'value' properties

    Example with object value:
        {
            "column": {"title": "Date", "type": "DATE"},
            "operator": "EQUAL",
            "values": [{"objectType": "DATE", "value": "2024-01-01"}]
        }
    """

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportFilterCriterion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column = TypedObject(ReportColumnIdentifier)
        self._operator = EnumeratedValue(ReportFilterOperator)
        self._values = None

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def column(self) -> Optional[ReportColumnIdentifier]:
        return self._column.value

    @column.setter
    def column(self, value: Union[ReportColumnIdentifier, dict]) -> None:
        self._column.value = value

    @property
    def operator(self) -> EnumeratedValue:
        return self._operator

    @operator.setter
    def operator(self, value: Union[ReportFilterOperator, str]) -> None:
        self._operator.set(value)

    @property
    def values(self) -> Optional[List[Union[str, int, float, dict, None]]]:
        """List of filter values.

        Can contain:
        - strings
        - numbers (int or float)
        - None (null)
        - dicts with 'objectType' and 'value' keys for special values like dates
        """
        return self._values

    @values.setter
    def values(self, value: List[Union[str, int, float, dict, None]]) -> None:
        if isinstance(value, list):
            self._values = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
