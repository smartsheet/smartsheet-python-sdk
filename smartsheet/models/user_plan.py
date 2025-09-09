class UserPlan:
    def __init__(self, plan_id=None, seat_type=None, seat_type_last_changed_at=None, is_internal=False):
        self._plan_id = plan_id
        self._seat_type = seat_type
        self._seat_type_last_changed_at = seat_type_last_changed_at
        self._is_internal = is_internal

    def get_plan_id(self):
        return self._plan_id

    def set_plan_id(self, plan_id):
        self._plan_id = plan_id

    def get_seat_type(self):
        return self._seat_type

    def set_seat_type(self, seat_type):
        self._seat_type = seat_type

    def get_seat_type_last_changed_at(self):
        return self._seat_type_last_changed_at

    def set_seat_type_last_changed_at(self, seat_type_last_changed_at):
        self._seat_type_last_changed_at = seat_type_last_changed_at

    def is_internal(self):
        return self._is_internal

    def set_is_internal(self, is_internal):
        self._is_internal = is_internal