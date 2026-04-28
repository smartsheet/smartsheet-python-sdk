from enum import Enum

class SeatType(str, Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
    PROVISIONAL_MEMBER = 'PROVISIONAL_MEMBER'
    CONTRIBUTOR = 'CONTRIBUTOR'


class DowngradeSeatType(str, Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'
    CONTRIBUTOR = 'CONTRIBUTOR'


class UpgradeSeatType(str, Enum):
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
