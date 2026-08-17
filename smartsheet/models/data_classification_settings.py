# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from ..types import Boolean, Number, String, TypedList, TypedObject, json
from ..util import deserialize, serialize


class ApproverEntry:

    """Smartsheet ApproverEntry data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the ApproverEntry model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._type = String()
        self._ids = TypedList(int)

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, value):
        self._type.value = value

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
