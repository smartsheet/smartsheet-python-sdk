# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import EnumeratedValue, TypedList, json
from ..util import deserialize, serialize
from .data_classification_approver_entry import DataClassificationApproverEntry
from .enums import DataClassificationDowngradeApprovalMode
from .data_classification_label_approver_entry import DataClassificationLabelApproverEntry


class DataClassificationDowngradeApprovalSettings:

    """Smartsheet DataClassificationDowngradeApprovalSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DataClassificationDowngradeApprovalSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._mode = EnumeratedValue(DataClassificationDowngradeApprovalMode)
        self._approvers = TypedList(DataClassificationApproverEntry)
        self._label_approvers = TypedList(DataClassificationLabelApproverEntry)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode.set(value)

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
