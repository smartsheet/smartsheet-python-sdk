# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
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

from __future__ import absolute_import

from typing import Optional

from ..types import Boolean, String, TypedList, TypedObject, json
from ..util import deserialize, serialize

from .report_column import ReportColumn
from .report_scope_inclusion import ReportScopeInclusion
from .report_destination import ReportDestination
from .report_definition import ReportDefinition


class CreateReportRequest:
    """Smartsheet CreateReportRequest data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the CreateReportRequest model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._name = String()
        self._columns = TypedList(ReportColumn)
        self._scope = TypedList(ReportScopeInclusion)
        self._report_definition = TypedObject(ReportDefinition)
        self._is_summary_report = Boolean()
        self._destination = TypedObject(ReportDestination)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def name(self) -> Optional[str]:
        return self._name.value

    @name.setter
    def name(self, value: str) -> None:
        self._name.value = value

    @property
    def columns(self) -> TypedList:
        return self._columns

    @columns.setter
    def columns(self, value) -> None:
        self._columns.load(value)

    @property
    def scope(self) -> TypedList:
        return self._scope

    @scope.setter
    def scope(self, value) -> None:
        self._scope.load(value)

    @property
    def report_definition(self):
        return self._report_definition.value

    @report_definition.setter
    def report_definition(self, value) -> None:
        self._report_definition.value = value

    @property
    def is_summary_report(self) -> Optional[bool]:
        return self._is_summary_report.value

    @is_summary_report.setter
    def is_summary_report(self, value: bool) -> None:
        self._is_summary_report.value = value

    @property
    def destination(self):
        return self._destination.value

    @destination.setter
    def destination(self, value) -> None:
        self._destination.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
