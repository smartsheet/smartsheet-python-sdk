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

from typing import TypeVar, List
from ..types import String, json, TypedList, importlib
from ..util import deserialize, serialize
from .asset_share import AssetShare

T = TypeVar('T')


class AssetSharesPaginatedResult:
    """Smartsheet AssetSharesPaginatedResult data model with generic type support.
    Use only for deserializing the response from GET /2.0/shares.
    Created because GET /2.0/shares returns items in the response body instead of data.
    As a result TokenPaginatedResult cannot be used.
    """

    def __init__(self, props=None, dynamic_data_type=None, base_obj=None):
        """Initialize the TokenPaginatedResult model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._dynamic_data_type = None
        if dynamic_data_type is not None:
            self._dynamic_data_type = dynamic_data_type

        self._items = TypedList(object)
        self._last_key = String()

        if props:
            deserialize(self, props)

        self.request_response = None
        self.__initialized = True

    @property
    def items(self) -> List[AssetShare]:
        return self._items

    @items.setter
    def items(self, value):
        class_ = getattr(
            importlib.import_module("smartsheet.models"), self._dynamic_data_type
        )
        if isinstance(value, list):
            self._items = [class_(x, self._base) for x in value]
        else:
            self._items = class_(value, self._base)


    @property
    def last_key(self):
        return self._last_key.value

    @last_key.setter
    def last_key(self, value):
        self._last_key.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
