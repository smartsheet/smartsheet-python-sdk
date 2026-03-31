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

from typing import Union

from ..types import EnumeratedValue, TypedList, json
from ..util import deserialize, serialize
from .enums import ReportBooleanOperator
from .report_filter_criterion import ReportFilterCriterion


class ReportFilterExpression:
    """Smartsheet ReportFilterExpression data model.

    An expression to filter on report columns. It is a recursive object that allows
    at most three levels.

    It must include 'operator' and at least one of the following: 'criteria' or 'nestedCriteria'

    Here is a two-level example:

        {
          "operator": "OR",
          "nestedCriteria": [
            {
              "operator": "AND",
              "criteria": [
                {
                  "column": { "title": "Price", "type": "TEXT_NUMBER" },
                  "operator": "GREATER_THAN",
                  "values": ["11"]
                },
                {
                  "column": { "primary": true },
                  "operator": "CONTAINS",
                  "values": ["PROJ-1"]
                }
              ]
            },
            {
              "operator": "AND",
              "criteria": [
                {
                  "column": { "title": "Quantity", "type": "TEXT_NUMBER" },
                  "operator": "LESS_THAN",
                  "values": ["12"]
                },
                {
                  "column": { "title": "Sold Out", "type": "CHECKBOX" },
                  "operator": "IS_CHECKED"
                }
              ]
            }
          ]
        }

    It's equivalent to the following pseudo logic:

        ("Price" > 11 AND "Primary" CONTAINS "PROJ-1")
        OR
        ("Quantity" < 12 AND "Sold Out" IS_CHECKED)
    """

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportFilterExpression model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._operator = EnumeratedValue(ReportBooleanOperator)
        self._nested_criteria = TypedList(ReportFilterExpression)
        self._criteria = TypedList(ReportFilterCriterion)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def operator(self) -> EnumeratedValue:
        return self._operator

    @operator.setter
    def operator(self, value: Union[ReportBooleanOperator, str]) -> None:
        self._operator.set(value)

    @property
    def nested_criteria(self) -> TypedList:
        return self._nested_criteria

    @nested_criteria.setter
    def nested_criteria(self, value: list) -> None:
        self._nested_criteria.load(value)

    @property
    def criteria(self) -> TypedList:
        return self._criteria

    @criteria.setter
    def criteria(self, value: list) -> None:
        self._criteria.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
