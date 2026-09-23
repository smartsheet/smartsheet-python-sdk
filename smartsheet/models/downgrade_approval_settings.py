# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import String, TypedList, json
from ..util import deserialize, serialize
from .approver_entry import ApproverEntry
from .label_approver_entry import LabelApproverEntry


class DowngradeApprovalSettings:

    """Smartsheet DowngradeApprovalSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DowngradeApprovalSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._mode = String()
        self._approvers = TypedList(ApproverEntry)
        self._label_approvers = TypedList(LabelApproverEntry)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def mode(self):
        return self._mode.value

    @mode.setter
    def mode(self, value):
        self._mode.value = value

    @property
    def approvers(self):
        return self._approvers

    @approvers.setter
    def approvers(self, value):
        self._approvers.load(value)

    @property
    def label_approvers(self):
        return self._label_approvers

    @label_approvers.setter
    def label_approvers(self, value):
        self._label_approvers.load(value)

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
