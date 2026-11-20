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

from ..types import EnumeratedValue, TypedList, json
from ..util import deserialize, serialize
from .enums import DataClassificationApproverType


class DataClassificationApproverEntry:

    """Smartsheet DataClassificationApproverEntry data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DataClassificationApproverEntry model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._type = EnumeratedValue(DataClassificationApproverType)
        self._ids = TypedList(int)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type.set(value)

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, value):
        self._ids.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
