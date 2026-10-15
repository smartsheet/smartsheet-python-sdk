# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import String, TypedList, json
from ..util import deserialize, serialize
from .approver_entry import ApproverEntry


class LabelApproverEntry:

    """Smartsheet LabelApproverEntry data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the LabelApproverEntry model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._label_id = String()
        self._approvers = TypedList(ApproverEntry)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def label_id(self):
        return self._label_id.value

    @label_id.setter
    def label_id(self, value):
        self._label_id.value = value

    @property
    def approvers(self):
        return self._approvers

    @approvers.setter
    def approvers(self, value):
        self._approvers.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
