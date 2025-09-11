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

from ..types import Boolean, Number, String, Timestamp, TypedList, TypedObject, json
from ..util import deserialize, serialize
from .report import Report
from .sheet import Sheet
from .sight import Sight
from .source import Source
from .template import Template


class Folder:

    """Smartsheet Folder data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Folder model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._created_at = Timestamp()
        self._favorite = Boolean()
        self._folders = TypedList(Folder)
        self._id_ = Number()
        self._modified_at = Timestamp()
        self._name = String()
        self._permalink = String()
        self._reports = TypedList(Report)
        self._sheets = TypedList(Sheet)
        self._sights = TypedList(Sight)
        self._source = TypedObject(Source)
        self._templates = TypedList(Template)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None
        self.__initialized = True

    def __getattr__(self, key):
        if key == "id":
            return self.id_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == "id":
            self.id_ = value
        else:
            super().__setattr__(key, value)

    @property
    def created_at(self):
        return self._created_at.value

    @created_at.setter
    def created_at(self, value):
        self._created_at.value = value

    @property
    def favorite(self):
        return self._favorite.value

    @favorite.setter
    def favorite(self, value):
        self._favorite.value = value

    @property
    def folders(self):
        return self._folders

    @folders.setter
    def folders(self, value):
        self._folders.load(value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def modified_at(self):
        return self._modified_at.value

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at.value = value

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

    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, value):
        self._reports.load(value)

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, value):
        self._sheets.load(value)

    @property
    def sights(self):
        return self._sights

    @sights.setter
    def sights(self, value):
        self._sights.load(value)

    @property
    def source(self):
        return self._source.value

    @source.setter
    def source(self, value):
        self._source.value = value

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates.load(value)

    def create_folder(self, folder_obj):
        return self._base.Folders.create_folder_in_folder(self.id, folder_obj)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
