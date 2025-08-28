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

from typing import Union
from ..util import deserialize
from .token_paginated_result import TokenPaginatedResult
from .folder import Folder
from .sheet import Sheet
from .sight import Sight
from .report import Report

# Type alias for children that can be any of these types
ChildType = Union[Folder, Sheet, Sight, Report]


class PaginatedChildrenResult(TokenPaginatedResult[ChildType]):
    """Smartsheet PaginatedChildrenResult that deserializes mixed children based on resourceType."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the PaginatedChildrenResult model."""
        super().__init__(props=None, base_obj=base_obj)

        if props:
            self._deserialize_data(props)
            deserialize(self, props)

    def _deserialize_data(self, props):
        """Custom deserialization for data array based on resourceType."""
        if 'data' in props:
            self._data = []
            for item in props['data']:
                self.append_data(item)

    def append_data(self, item):
        """Append data item, converting to appropriate model based on resourceType."""
        # Get resource type from either dict or object
        if isinstance(item, dict):
            resource_type = item.get('resourceType', '').lower()
        else:
            resource_type = getattr(item, 'resourceType', '').lower()

        # Convert to appropriate model object based on resource type
        if resource_type == 'folder':
            self._data.append(Folder(item, self._base))
        elif resource_type == 'sheet':
            self._data.append(Sheet(item, self._base))
        elif resource_type == 'sight':
            self._data.append(Sight(item, self._base))
        elif resource_type == 'report':
            self._data.append(Report(item, self._base))
        else:
            # If no resource type or unknown type, append as-is
            self._data.append(item)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        """Custom setter that handles deserialization of mixed resource types."""
        self._data = []
        for item in value:
            self.append_data(item)
