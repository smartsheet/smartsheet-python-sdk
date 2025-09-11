from enum import Enum

class SeatType(Enum):
    VIEWER = 'VIEWER'
    GUEST = 'GUEST'
    MEMBER = 'MEMBER'
    PROVISIONAL_MEMBER = 'PROVISIONAL_MEMBER'