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

from ..types import TypedList, TypedObject, json
from ..util import deserialize, serialize
from .report_summarizing_criterion import ReportSummarizingCriterion
from .report_filter_expression import ReportFilterExpression
from .report_grouping_criterion import ReportGroupingCriterion
from .report_sorting_criterion import ReportSortingCriterion


class ReportDefinition:
    """Smartsheet ReportDefinition data model.

    The report definition contains filters, grouping and sorting properties of the report.

    Note: When groupingCriteria is defined the primary column of the report will move
    to index 0 when it is first rendered by the app.

    Supports partial updates on root level properties such as:
    - filters
    - groupingCriteria
    - summarizingCriteria
    - sortingCriteria
    """

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportDefinition model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._filters = TypedObject(ReportFilterExpression)
        self._grouping_criteria = TypedList(ReportGroupingCriterion)
        self._summarizing_criteria = TypedList(ReportSummarizingCriterion)
        self._sorting_criteria = TypedList(ReportSortingCriterion)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def filters(self):
        return self._filters.value

    @filters.setter
    def filters(self, value):
        self._filters.value = value

    @property
    def grouping_criteria(self):
        return self._grouping_criteria

    @grouping_criteria.setter
    def grouping_criteria(self, value):
        self._grouping_criteria.load(value)

    @property
    def summarizing_criteria(self):
        return self._summarizing_criteria

    @summarizing_criteria.setter
    def summarizing_criteria(self, value):
        self._summarizing_criteria.load(value)

    @property
    def sorting_criteria(self):
        return self._sorting_criteria

    @sorting_criteria.setter
    def sorting_criteria(self, value):
        self._sorting_criteria.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
