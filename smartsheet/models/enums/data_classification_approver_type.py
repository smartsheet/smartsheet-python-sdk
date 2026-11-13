from enum import Enum

class DataClassificationApproverType(str, Enum):
    GROUPS = 'GROUPS'
    USERS = 'USERS'
    WORKSPACE_ADMINS = 'WORKSPACE_ADMINS'
