from enum import Enum

class SeatType(str, Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
    PROVISIONAL_MEMBER = 'PROVISIONAL_MEMBER'
