from enum import Enum

class AssetType(str, Enum):
    """Defines the asset types supported by the Sharing API."""
    SHEET = 'sheet'
    REPORT = 'report'
    SIGHT = 'sight'
    WORKSPACE = 'workspace'
    COLLECTION = 'collection'
    FILE = 'file'
