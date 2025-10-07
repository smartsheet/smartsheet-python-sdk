from __future__ import absolute_import

from ..types import (Boolean, EnumeratedValue, Number, String, Timestamp,
                     TypedList, TypedObject, json)
from ..models.enums import SeatType
from ..util import deserialize, serialize


class UserPlan:

    """Smartsheet Plan for a User data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the UserPlan model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj

        self._plan_id = Number()
        self._seat_type = EnumeratedValue(SeatType)
        self._seat_type_last_changed_at = Timestamp()
        self._is_internal = Boolean()
        self._provisional_expiration_date = Timestamp()

        if props:
            deserialize(self, props)

        self.__initialized = True

    @property
    def plan_id(self):
        return self._plan_id.value

    @plan_id.setter
    def plan_id(self, value):
        self._plan_id.value = value

    @property
    def seat_type(self):
        return self._seat_type

    @seat_type.setter
    def seat_type(self, value):
        self._seat_type.set(value)

    @property
    def seat_type_last_changed_at(self):
        return self._seat_type_last_changed_at.value

    @seat_type_last_changed_at.setter
    def seat_type_last_changed_at(self, value):
        self._seat_type_last_changed_at.value = value

    @property
    def is_internal(self):
        return self._is_internal.value

    @is_internal.setter
    def is_internal(self, value):
        self._is_internal.value = value

    @property
    def provisional_expiration_date(self):
        return self._provisional_expiration_date.value

    @provisional_expiration_date.setter
    def provisional_expiration_date(self, value):
        self._provisional_expiration_date.value = value

    def to_dict(self):
        return serialize(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()
