from enum import Enum

class ApproverType(str, Enum):
    GROUPS = 'GROUPS'
    USERS = 'USERS'
    WORKSPACE_ADMINS = 'WORKSPACE_ADMINS'
