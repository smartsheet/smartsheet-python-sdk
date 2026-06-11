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

from ..types import TypedList
from ..util import deserialize
from .path_leaf import PathLeaf
from .path_node import PathNode


class SheetPathNode(PathNode):

    """Node in a sheet path response. Contains recursive folders leading to the target sheet."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SheetPathNode model."""
        super().__init__(props=None, base_obj=base_obj)

        self._folders = TypedList(SheetPathNode)
        self._sheets = TypedList(PathLeaf)

        if props:
            deserialize(self, props)

    @property
    def folders(self):
        return self._folders

    @folders.setter
    def folders(self, value):
        self._folders.load(value)

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, value):
        self._sheets.load(value)

    def get_leaf_sheet(self):
        """Return the target PathLeaf sheet, or None if not reachable."""
        if self.sheets:
            return self.sheets[0]
        if self.folders:
            return self.folders[0].get_leaf_sheet()
        return None

    def get_leaf_sheet_path(self):
        """Return a Unix-style path string from this node to the target sheet.
            Example: '/Workspace/Folder/Sheet'
        """
        if self.sheets:
            return f"/{self.name}/{self.sheets[0].name}"
        if self.folders:
            return f"/{self.name}{self.folders[0].get_leaf_sheet_path()}"
        return None
