# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import EnumeratedValue, TypedList, json
from ..util import deserialize, serialize
from .enums import ApproverType


class ApproverEntry:

    """Smartsheet ApproverEntry data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ApproverEntry model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._type = EnumeratedValue(ApproverType)
        self._ids = TypedList(int)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type.set(value)

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, value):
        self._ids.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
