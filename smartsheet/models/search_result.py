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

from ..types import Number, TypedList, json
from ..util import deserialize, serialize
from .search_result_item import SearchResultItem


class SearchResult:

    """Smartsheet SearchResult data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the SearchResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._results = TypedList(SearchResultItem)
        self._total_count = Number()

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results.load(value)

    @property
    def total_count(self):
        return self._total_count.value

    @total_count.setter
    def total_count(self, value):
        self._total_count.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
