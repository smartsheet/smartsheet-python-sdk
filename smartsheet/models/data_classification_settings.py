# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import Boolean, Number, String, TypedList, TypedObject, json
from ..util import deserialize, serialize
from .classification_label import ClassificationLabel
from .downgrade_approval_settings import DowngradeApprovalSettings


class DataClassificationSettings:

    """Smartsheet DataClassificationSettings data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the DataClassificationSettings model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._org_id = Number()
        self._plan_id = Number()
        self._is_disabled = Boolean()
        self._guidelines_url = String()
        self._allow_manual_change = Boolean()
        self._labels = TypedList(ClassificationLabel)
        self._downgrade_approval_settings = TypedObject(DowngradeApprovalSettings)

        if props:
            deserialize(self, props)

        # requests package Response object
        self.request_response = None

        self.__initialized = True

    @property
    def org_id(self):
        return self._org_id.value

    @org_id.setter
    def org_id(self, value):
        self._org_id.value = value

    @property
    def plan_id(self):
        return self._plan_id.value

    @plan_id.setter
    def plan_id(self, value):
        self._plan_id.value = value

    @property
    def is_disabled(self):
        return self._is_disabled.value

    @is_disabled.setter
    def is_disabled(self, value):
        self._is_disabled.value = value

    @property
    def guidelines_url(self):
        return self._guidelines_url.value

    @guidelines_url.setter
    def guidelines_url(self, value):
        self._guidelines_url.value = value

    @property
    def allow_manual_change(self):
        return self._allow_manual_change.value

    @allow_manual_change.setter
    def allow_manual_change(self, value):
        self._allow_manual_change.value = value

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        self._labels.load(value)

    @property
    def downgrade_approval_settings(self):
        return self._downgrade_approval_settings.value

    @downgrade_approval_settings.setter
    def downgrade_approval_settings(self, value):
        self._downgrade_approval_settings.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
