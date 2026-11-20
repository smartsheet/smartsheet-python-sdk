# pylint: disable=C0111,R0902,R0904,W0212,W0221
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

from ..types import String, TypedList, json
from ..util import deserialize, serialize
from .data_classification_approver_entry import DataClassificationApproverEntry


class DataClassificationLabelApproverEntry:

    """Smartsheet DataClassificationLabelApproverEntry data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DataClassificationLabelApproverEntry model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._label_id = String()
        self._approvers = TypedList(DataClassificationApproverEntry)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def label_id(self):
        return self._label_id.value

    @label_id.setter
    def label_id(self, value):
        self._label_id.value = value

    @property
    def approvers(self):
        return self._approvers

    @approvers.setter
    def approvers(self, value):
        self._approvers.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
