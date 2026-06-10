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


class ReportPathNode(PathNode):

    """Node in a report path response. Contains recursive folders leading to the target report."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ReportPathNode model."""
        super().__init__(props=None, base_obj=base_obj)

        self._folders = TypedList(ReportPathNode)
        self._reports = TypedList(PathLeaf)

        if props:
            deserialize(self, props)

    @property
    def folders(self):
        return self._folders

    @folders.setter
    def folders(self, value):
        self._folders.load(value)

    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, value):
        self._reports.load(value)

    def _walk_to_leaf(self):
        """Yield each node from self down to the node containing the target report."""
        node = self
        while True:
            yield node
            if node._reports:
                break
            if node._folders:
                node = node._folders[0]
            else:
                break

    def get_report(self):
        """Return the target PathLeaf report, or None if not reachable."""
        for node in self._walk_to_leaf():
            if node._reports:
                return node._reports[0]
        return None

    def get_report_path(self):
        """Return a Unix-style path string from this node to the target report."""
        nodes = list(self._walk_to_leaf())
        if not nodes:
            return None
        parts = [n.name for n in nodes if n.name]
        leaf = nodes[-1]
        if leaf._reports and leaf._reports[0].name:
            parts[-1] = leaf._reports[0].name
        return "/".join(parts) if parts else None
