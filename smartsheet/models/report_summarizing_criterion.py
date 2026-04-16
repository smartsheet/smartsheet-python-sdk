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

from ..types import EnumeratedValue, TypedObject, json
from ..util import deserialize, serialize
from .enums import ReportAggregationType
from .report_column_identifier import ReportColumnIdentifier


class ReportSummarizingCriterion:
    """Smartsheet ReportSummarizingCriterion data model.

    Report summarizing criterion. Requires 'column' and 'aggregationType'.
    """

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportSummarizingCriterion model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._column = TypedObject(ReportColumnIdentifier)
        self._aggregation_type = EnumeratedValue(ReportAggregationType)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def column(self) -> Optional[ReportColumnIdentifier]:
        """Column to summarize."""
        return self._column.value

    @column.setter
    def column(self, value: Union[ReportColumnIdentifier, dict]) -> None:
        self._column.value = value

    @property
    def aggregation_type(self) -> EnumeratedValue:
        """Type of aggregation (SUM, AVG, MIN, MAX, COUNT, FIRST, LAST)."""
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, value: Union[ReportAggregationType, str]) -> None:
        self._aggregation_type.set(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
