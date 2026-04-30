# pylint: disable=C0103,W0212
"""Unit tests for the EnumeratedValue.set() method in smartsheet/types.py"""

from smartsheet.types import EnumeratedValue
from smartsheet.models.enums.access_level import AccessLevel
from smartsheet.models.enums.report_asset_type import ReportAssetType
from smartsheet.models.enums.report_destination_type import ReportDestinationType


class TestEnumeratedValueSetByName:
    """Test setting EnumeratedValue by enum member name"""

    def test_set_by_valid_name(self):
        """Test setting value using valid enum member name"""
        enum_val = EnumeratedValue(AccessLevel)
        enum_val.set("VIEWER")
        assert enum_val.value == AccessLevel.VIEWER
        assert str(enum_val) == "VIEWER"

    def test_set_by_different_valid_names(self):
        """Test setting value using different valid enum member names"""
        enum_val = EnumeratedValue(AccessLevel)

        enum_val.set("COMMENTER")
        assert enum_val.value == AccessLevel.COMMENTER

        enum_val.set("EDITOR")
        assert enum_val.value == AccessLevel.EDITOR

        enum_val.set("ADMIN")
        assert enum_val.value == AccessLevel.ADMIN

        enum_val.set("OWNER")
        assert enum_val.value == AccessLevel.OWNER

    def test_set_by_name_with_underscore(self):
        """Test setting value using enum member name containing underscore"""
        enum_val = EnumeratedValue(AccessLevel)
        enum_val.set("EDITOR_SHARE")
        assert enum_val.value == AccessLevel.EDITOR_SHARE
        assert str(enum_val) == "EDITOR_SHARE"

    def test_set_by_name_overwrites_previous_value(self):
        """Test that setting by name overwrites the previous value"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("ADMIN")
        assert enum_val.value == AccessLevel.ADMIN
        assert str(enum_val) == "ADMIN"


class TestEnumeratedValueSetByEnum:
    """Test setting EnumeratedValue by passing an Enum instance"""

    def test_set_by_enum_instance(self):
        """Test setting value using an Enum instance directly"""
        enum_val = EnumeratedValue(AccessLevel)
        enum_val.set(AccessLevel.EDITOR)
        assert enum_val.value == AccessLevel.EDITOR
        assert str(enum_val) == "EDITOR"

    def test_set_by_different_enum_instances(self):
        """Test setting value using different Enum instances"""
        enum_val = EnumeratedValue(AccessLevel)

        enum_val.set(AccessLevel.VIEWER)
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(AccessLevel.ADMIN)
        assert enum_val.value == AccessLevel.ADMIN

        enum_val.set(AccessLevel.OWNER)
        assert enum_val.value == AccessLevel.OWNER

    def test_set_by_enum_overwrites_previous_value(self):
        """Test that setting by Enum instance overwrites the previous value"""
        enum_val = EnumeratedValue(AccessLevel, AccessLevel.VIEWER)
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(AccessLevel.COMMENTER)
        assert enum_val.value == AccessLevel.COMMENTER
        assert str(enum_val) == "COMMENTER"


class TestEnumeratedValueSetInvalidInputs:
    """Test setting EnumeratedValue with invalid inputs returns None"""

    def test_set_with_invalid_name_returns_none(self):
        """Test setting with an invalid enum member name returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("INVALID_NAME")
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_invalid_value_returns_none(self):
        """Test setting with an invalid enum value returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(999)
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_lowercase_name_returns_none(self):
        """Test setting with lowercase name (not matching exact case) returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        # Python enum names are case-sensitive
        enum_val.set("viewer")
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_partial_name_returns_none(self):
        """Test setting with partial enum name returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("VIEW")
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_integer_type_returns_none(self):
        """Test setting with integer type (not string) returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        # set() expects string or Enum, not raw int
        enum_val.set(1)
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_none_returns_none(self):
        """Test setting with None returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(None)
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_empty_string_returns_none(self):
        """Test setting with empty string returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("")
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_dict_returns_none(self):
        """Test setting with dict type returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set({"key": "value"})
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_with_list_returns_none(self):
        """Test setting with list type returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(["VIEWER"])
        assert enum_val.value is None
        assert str(enum_val) == "None"


class TestEnumeratedValueSetInitialization:
    """Test that set() is called during initialization"""

    def test_initialization_with_name(self):
        """Test initialization with enum member name"""
        enum_val = EnumeratedValue(AccessLevel, "EDITOR")
        assert enum_val.value == AccessLevel.EDITOR

    def test_initialization_with_value(self):
        """Test initialization with enum member value"""
        enum_val = EnumeratedValue(ReportDestinationType, "workspace")
        assert enum_val.value == ReportDestinationType.WORKSPACE

    def test_initialization_with_enum(self):
        """Test initialization with Enum instance"""
        enum_val = EnumeratedValue(AccessLevel, AccessLevel.EDITOR)
        assert enum_val.value == AccessLevel.EDITOR

    def test_initialization_with_invalid_returns_none(self):
        """Test initialization with invalid value returns None"""
        enum_val = EnumeratedValue(AccessLevel, "INVALID")
        assert enum_val.value is None

    def test_initialization_without_value(self):
        """Test initialization without value leaves it as None"""
        enum_val = EnumeratedValue(AccessLevel)
        assert enum_val.value is None


class TestEnumeratedValueSetStringBasedEnums:
    """Test setting EnumeratedValue with string-based enums where value != name

    This tests the fallback path where we set by the enum's value (e.g., 'sheet')
    rather than its name (e.g., 'SHEET'). This validates that the set() function
    correctly tries name lookup first, then falls back to value lookup.
    """

    def test_set_by_string_value_sheet(self):
        """Test setting ReportAssetType by string value 'sheet' (not name 'SHEET')"""
        enum_val = EnumeratedValue(ReportAssetType)
        # Setting by the enum value 'sheet' (lowercase), not the name 'SHEET'
        enum_val.set("sheet")
        assert enum_val.value == ReportAssetType.SHEET
        assert str(enum_val) == "SHEET"

    def test_set_by_string_value_workspace(self):
        """Test setting ReportAssetType by string value 'workspace' (not name 'WORKSPACE')"""
        enum_val = EnumeratedValue(ReportAssetType)
        enum_val.set("workspace")
        assert enum_val.value == ReportAssetType.WORKSPACE
        assert str(enum_val) == "WORKSPACE"

    def test_set_by_name_vs_value_for_string_enum(self):
        """Test that name lookup is tried first, then value lookup for string enums"""
        enum_val = EnumeratedValue(ReportAssetType)

        # Set by NAME (uppercase)
        enum_val.set("SHEET")
        assert enum_val.value == ReportAssetType.SHEET
        assert str(enum_val) == "SHEET"

        # Set by VALUE (lowercase)
        enum_val.set("sheet")
        assert enum_val.value == ReportAssetType.SHEET
        assert str(enum_val) == "SHEET"

        # Both should work and map to the same enum member

    def test_set_report_destination_by_value(self):
        """Test setting ReportDestinationType by string values"""
        enum_val = EnumeratedValue(ReportDestinationType)

        # Set by value 'workspace'
        enum_val.set("workspace")
        assert enum_val.value == ReportDestinationType.WORKSPACE
        assert str(enum_val) == "WORKSPACE"

        # Set by value 'folder'
        enum_val.set("folder")
        assert enum_val.value == ReportDestinationType.FOLDER
        assert str(enum_val) == "FOLDER"

    def test_set_report_destination_by_name(self):
        """Test setting ReportDestinationType by enum member names"""
        enum_val = EnumeratedValue(ReportDestinationType)

        # Set by NAME 'WORKSPACE'
        enum_val.set("WORKSPACE")
        assert enum_val.value == ReportDestinationType.WORKSPACE

        # Set by NAME 'FOLDER'
        enum_val.set("FOLDER")
        assert enum_val.value == ReportDestinationType.FOLDER

    def test_set_string_enum_invalid_value_returns_none(self):
        """Test setting with invalid string value returns None"""
        enum_val = EnumeratedValue(ReportAssetType, "sheet")
        assert enum_val.value == ReportAssetType.SHEET

        # Try invalid value
        enum_val.set("invalid_asset")
        assert enum_val.value is None
        assert str(enum_val) == "None"

    def test_set_string_enum_case_sensitive(self):
        """Test that string enum values are case-sensitive

        'Sheet' or 'SHEET' won't match the value 'sheet' unless it's the name 'SHEET'
        """
        enum_val = EnumeratedValue(ReportAssetType)

        # NAME 'SHEET' should work
        enum_val.set("SHEET")
        assert enum_val.value == ReportAssetType.SHEET

        # value 'sheet' should work
        enum_val.set("sheet")
        assert enum_val.value == ReportAssetType.SHEET

        # Mixed case 'Sheet' should NOT work (not a valid name or value)
        enum_val.set("Sheet")
        assert enum_val.value is None

    def test_set_string_enum_initialization(self):
        """Test initialization with string-based enum values"""
        # Initialize with value
        enum_val1 = EnumeratedValue(ReportAssetType, "sheet")
        assert enum_val1.value == ReportAssetType.SHEET

        # Initialize with name
        enum_val2 = EnumeratedValue(ReportAssetType, "SHEET")
        assert enum_val2.value == ReportAssetType.SHEET

        # Both should result in the same enum member

    def test_set_string_enum_multiple_switches(self):
        """Test switching between different enum values for string-based enums"""
        enum_val = EnumeratedValue(ReportAssetType)

        # Set by value
        enum_val.set("sheet")
        assert enum_val.value == ReportAssetType.SHEET

        # Set by name
        enum_val.set("WORKSPACE")
        assert enum_val.value == ReportAssetType.WORKSPACE

        # Set by value again
        enum_val.set("sheet")
        assert enum_val.value == ReportAssetType.SHEET

        # Set by enum instance
        enum_val.set(ReportAssetType.WORKSPACE)
        assert enum_val.value == ReportAssetType.WORKSPACE


class TestEnumeratedValueSetEdgeCases:
    """Test edge cases for the set() method"""

    def test_set_multiple_times_in_sequence(self):
        """Test setting value multiple times in sequence"""
        enum_val = EnumeratedValue(AccessLevel)

        enum_val.set("VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("EDITOR")
        assert enum_val.value == AccessLevel.EDITOR

        enum_val.set(AccessLevel.ADMIN)
        assert enum_val.value == AccessLevel.ADMIN

        enum_val.set(AccessLevel.OWNER)
        assert enum_val.value == AccessLevel.OWNER

        enum_val.set("INVALID")
        assert enum_val.value is None

    def test_set_with_whitespace_string_returns_none(self):
        """Test setting with whitespace-only string returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set("   ")
        assert enum_val.value is None

    def test_set_with_name_containing_extra_whitespace_returns_none(self):
        """Test setting with name containing extra whitespace returns None"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        assert enum_val.value == AccessLevel.VIEWER

        enum_val.set(" VIEWER ")
        assert enum_val.value is None
        assert str(enum_val) == "None"
