from typing import List


class UserPlansResponse:
    def __init__(self, data: List['UserPlan'] = None, last_key: str = None):
        self._data = data or []
        self._last_key = last_key

    def get_data(self) -> List['UserPlan']:
        return self._data

    def set_data(self, data: List['UserPlan']):
        self._data = data

    def get_last_key(self) -> str:
        return self._last_key

    def set_last_key(self, last_key: str):
        self._last_key = last_key