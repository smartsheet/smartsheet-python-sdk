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
from .path_node import PathNode


class FolderPathNode(PathNode):

    """Node in a folder path response. Contains recursive folders leading to the target folder."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the FolderPathNode model."""
        super().__init__(props=None, base_obj=base_obj)

        self._folders = TypedList(FolderPathNode)

        if props:
            deserialize(self, props)

    @property
    def folders(self):
        return self._folders

    @folders.setter
    def folders(self, value):
        self._folders.load(value)

    def _walk_to_leaf(self):
        """Yield each node from self down to the deepest folder (the target folder)."""
        node = self
        while True:
            yield node
            if node._folders:
                node = node._folders[0]
            else:
                break

    def get_folder(self):
        """Return the deepest FolderPathNode reachable from this node, or None if empty."""
        last = None
        for node in self._walk_to_leaf():
            last = node
        return last

    def get_folder_path(self):
        """Return a Unix-style path string of folder names from this node to the target folder."""
        nodes = list(self._walk_to_leaf())
        if not nodes:
            return None
        return "/".join(n.name for n in nodes if n.name)
