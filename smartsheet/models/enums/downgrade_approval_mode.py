from enum import Enum

class DowngradeApprovalMode(str, Enum):
    NONE = 'NONE'
    APPROVAL_NEEDED = 'APPROVAL_NEEDED'
    CUSTOM = 'CUSTOM'
