# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import Boolean, Number, String, json
from ..util import deserialize, serialize


class ClassificationLabel:

    """Smartsheet ClassificationLabel data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ClassificationLabel model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._id = String()
        self._name = String()
        self._description = String()
        self._color = String()
        self._sensitivity_order = Number()
        self._is_default = Boolean()

        if props:
            deserialize(self, props)

        self.__initialized = True

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
    def description(self):
        return self._description.value

    @description.setter
    def description(self, value):
        self._description.value = value

    @property
    def color(self):
        return self._color.value

    @color.setter
    def color(self, value):
        self._color.value = value

    @property
    def sensitivity_order(self):
        return self._sensitivity_order.value

    @sensitivity_order.setter
    def sensitivity_order(self, value):
        self._sensitivity_order.value = value

    @property
    def is_default(self):
        return self._is_default.value

    @is_default.setter
    def is_default(self, value):
        self._is_default.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
