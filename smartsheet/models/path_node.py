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

from ..types import EnumeratedValue, Number, String, json
from ..util import deserialize, serialize
from .enums import AccessLevel


class PathNode:
    """Base node in a Smartsheet path response (workspace root or intermediate folder)."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the PathNode model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._access_level = EnumeratedValue(AccessLevel)
        self._id = Number()
        self._name = String()
        self._permalink = String()

        if props:
            deserialize(self, props)

        self.request_response = None
        self.__initialized = True

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level.set(value)

    @property
    def id(self):
        return self._id.value

    @id.setter
    def id(self, value):
        self._id.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def permalink(self):
        return self._permalink.value

    @permalink.setter
    def permalink(self, value):
        self._permalink.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
