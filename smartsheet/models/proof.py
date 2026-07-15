# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
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

from ..types import Boolean, EnumeratedValue, Number, String, Timestamp, TypedList, TypedObject, json
from ..util import deserialize, serialize
from .attachment import Attachment
from .discussion import Discussion
from .enums import ProofType
from .user import User


class Proof:

    """Smartsheet Proof data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Proof model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._id_ = Number()
        self._original_id = Number()
        self._name = String()
        self._type_ = EnumeratedValue(ProofType)
        self._document_type = String()
        self._proof_request_url = String()
        self._version = Number()
        self._last_updated_at = Timestamp()
        self._last_updated_by = TypedObject(User)
        self._is_completed = Boolean()
        self._attachments = TypedList(Attachment)
        self._discussions = TypedList(Discussion)

        if props:
            deserialize(self, props)

        self.__initialized = True

    def __getattr__(self, key):
        if key == "id":
            return self.id_
        elif key == "type":
            return self.type_
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == "id":
            self.id_ = value
        elif key == "type":
            self.type_ = value
        else:
            super().__setattr__(key, value)

    @property
    def id_(self):
        return self._id_.value

    @id_.setter
    def id_(self, value):
        self._id_.value = value

    @property
    def original_id(self):
        return self._original_id.value

    @original_id.setter
    def original_id(self, value):
        self._original_id.value = value

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = value

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, value):
        self._type_.set(value)

    @property
    def document_type(self):
        return self._document_type.value

    @document_type.setter
    def document_type(self, value):
        self._document_type.value = value

    @property
    def proof_request_url(self):
        return self._proof_request_url.value

    @proof_request_url.setter
    def proof_request_url(self, value):
        self._proof_request_url.value = value

    @property
    def version(self):
        return self._version.value

    @version.setter
    def version(self, value):
        self._version.value = value

    @property
    def last_updated_at(self):
        return self._last_updated_at.value

    @last_updated_at.setter
    def last_updated_at(self, value):
        self._last_updated_at.value = value

    @property
    def last_updated_by(self):
        return self._last_updated_by.value

    @last_updated_by.setter
    def last_updated_by(self, value):
        self._last_updated_by.value = value
    @property
    def is_completed(self):
        return self._is_completed.value

    @is_completed.setter
    def is_completed(self, value):
        self._is_completed.value = value

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments.load(value)

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def discussions(self, value):
        self._discussions.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
