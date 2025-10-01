from enum import Enum

class SeatType(str, Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
    PROVISIONAL_MEMBER = 'PROVISIONAL_MEMBER'


class DowngradeSeatType(str, Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'


class UpgradeSeatType(str, Enum):
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
