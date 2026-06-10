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

from ..types import Timestamp
from ..util import deserialize
from .path_node import PathNode


class PathLeaf(PathNode):

    """Terminal asset node in a Smartsheet path response (sheet, report, sight, or target folder)."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the PathLeaf model."""
        super().__init__(props=None, base_obj=base_obj)

        self._created_at = Timestamp()
        self._modified_at = Timestamp()

        if props:
            deserialize(self, props)

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value
