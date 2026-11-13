from enum import Enum

class DataClassificationDowngradeApprovalMode(str, Enum):
    NONE = 'NONE'
    APPROVAL_NEEDED = 'APPROVAL_NEEDED'
    CUSTOM = 'CUSTOM'
