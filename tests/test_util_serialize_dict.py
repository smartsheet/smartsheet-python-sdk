# pylint: disable=C0103,W0212
"""Unit tests for the serialize function's dict handling in smartsheet/util.py"""

import pytest
from datetime import datetime, date
from smartsheet.util import serialize
from smartsheet.models import ExplicitNull
from smartsheet.types import EnumeratedValue
from smartsheet.models.enums.access_level import AccessLevel


class MockObjectWithSerialize:
    """Mock object with serialize method"""
    def serialize(self):
        return {"serialized": "data"}


class MockObjectWithToDict:
    """Mock object without serialize but with properties"""
    def __init__(self):
        self._name = "test"
    
    @property
    def name(self):
        return self._name


class TestSerializeDictBasic:
    """Test basic dict serialization scenarios"""
    
    def test_empty_dict(self):
        """Test serialization of an empty dict"""
        obj = {}
        result = serialize(obj)
        assert result == {}
        assert isinstance(result, dict)
    
    def test_dict_with_string_values(self):
        """Test dict with string values"""
        obj = {"key1": "value1", "key2": "value2"}
        result = serialize(obj)
        assert result == {"key1": "value1", "key2": "value2"}
    
    def test_dict_with_int_values(self):
        """Test dict with integer values"""
        obj = {"count": 42, "total": 100}
        result = serialize(obj)
        assert result == {"count": 42, "total": 100}
    
    def test_dict_with_float_values(self):
        """Test dict with float values"""
        obj = {"price": 19.99, "tax": 1.5}
        result = serialize(obj)
        assert result == {"price": 19.99, "tax": 1.5}
    
    def test_dict_with_bool_values(self):
        """Test dict with boolean values"""
        obj = {"active": True, "deleted": False}
        result = serialize(obj)
        assert result == {"active": True, "deleted": False}
    
    def test_dict_with_none_values(self):
        """Test dict with None values - preserved as None"""
        obj = {"key1": "value1", "key2": None, "key3": "value3"}
        result = serialize(obj)
        # None values should be preserved as None
        assert result == {"key1": "value1", "key2": None, "key3": "value3"}


class TestSerializeDictNested:
    """Test nested dict serialization scenarios"""
    
    def test_dict_with_nested_dict(self):
        """Test dict containing nested dicts"""
        obj = {
            "outer": {
                "inner": "value"
            }
        }
        result = serialize(obj)
        assert result == {"outer": {"inner": "value"}}
    
    def test_dict_with_deeply_nested_dicts(self):
        """Test dict with multiple levels of nesting"""
        obj = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        result = serialize(obj)
        assert result == obj
    
    def test_dict_with_nested_dict_containing_none(self):
        """Test nested dict with None values"""
        obj = {
            "outer": {
                "key1": "value1",
                "key2": None
            }
        }
        result = serialize(obj)
        # Inner None should be preserved as None
        assert result == {"outer": {"key1": "value1", "key2": None}}


class TestSerializeDictWithLists:
    """Test dict serialization with list values"""
    
    def test_dict_with_list_of_primitives(self):
        """Test dict containing list of primitive values"""
        obj = {"numbers": [1, 2, 3], "strings": ["a", "b", "c"]}
        result = serialize(obj)
        assert result == {"numbers": [1, 2, 3], "strings": ["a", "b", "c"]}
    
    def test_dict_with_empty_list(self):
        """Test dict with empty list - returns None which serializes to empty dict"""
        obj = {"key1": "value", "empty": []}
        result = serialize(obj)
        # Empty lists return None, which becomes None in the result
        assert result == {"key1": "value", "empty": None}
    
    def test_dict_with_list_of_dicts(self):
        """Test dict containing list of dicts"""
        obj = {
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"}
            ]
        }
        result = serialize(obj)
        assert result == obj


class TestSerializeDictWithDatetime:
    """Test dict serialization with datetime values"""
    
    def test_dict_with_datetime(self):
        """Test dict with datetime values"""
        dt = datetime(2023, 1, 15, 10, 30, 45)
        obj = {"created": dt}
        result = serialize(obj)
        assert result == {"created": dt.isoformat() + "Z"}
    
    def test_dict_with_date(self):
        """Test dict with date values"""
        d = date(2023, 1, 15)
        obj = {"date": d}
        result = serialize(obj)
        assert result == {"date": d.isoformat()}
    
    def test_dict_with_mixed_datetime_and_primitives(self):
        """Test dict with both datetime and primitive values"""
        dt = datetime(2023, 1, 15, 10, 30, 45)
        obj = {"created": dt, "name": "test", "count": 5}
        result = serialize(obj)
        assert result == {
            "created": dt.isoformat() + "Z",
            "name": "test",
            "count": 5
        }


class TestSerializeDictWithExplicitNull:
    """Test dict serialization with ExplicitNull values"""
    
    def test_dict_with_explicit_null(self):
        """Test dict with ExplicitNull - should be excluded"""
        obj = {"key1": "value1", "key2": ExplicitNull()}
        result = serialize(obj)
        # ExplicitNull values should be excluded
        assert result == {"key1": "value1"}
        assert "key2" not in result
    
    def test_dict_with_only_explicit_null(self):
        """Test dict containing only ExplicitNull"""
        obj = {"null_key": ExplicitNull()}
        result = serialize(obj)
        assert result == {}
    
    def test_dict_with_nested_explicit_null(self):
        """Test nested dict with ExplicitNull"""
        obj = {
            "outer": {
                "key1": "value",
                "key2": ExplicitNull()
            }
        }
        result = serialize(obj)
        assert result == {"outer": {"key1": "value"}}


class TestSerializeDictWithEnumeratedValue:
    """Test dict serialization with EnumeratedValue"""
    
    def test_dict_with_enumerated_value(self):
        """Test dict with EnumeratedValue"""
        enum_val = EnumeratedValue(AccessLevel, "VIEWER")
        obj = {"access": enum_val}
        result = serialize(obj)
        assert result == {"access": "VIEWER"}
    
    def test_dict_with_none_enumerated_value(self):
        """Test dict with EnumeratedValue that has None value"""
        enum_val = EnumeratedValue(AccessLevel)
        obj = {"access": enum_val}
        result = serialize(obj)
        # EnumeratedValue with None returns None
        assert result == {"access": None}


class TestSerializeDictWithObjects:
    """Test dict serialization with custom objects"""
    
    def test_dict_with_object_having_serialize(self):
        """Test dict with object that has serialize method"""
        mock_obj = MockObjectWithSerialize()
        obj = {"data": mock_obj}
        result = serialize(obj)
        assert result == {"data": {"serialized": "data"}}
    
    def test_dict_with_mixed_objects_and_primitives(self):
        """Test dict with both objects and primitives"""
        mock_obj = MockObjectWithSerialize()
        obj = {
            "name": "test",
            "count": 42,
            "data": mock_obj
        }
        result = serialize(obj)
        assert result == {
            "name": "test",
            "count": 42,
            "data": {"serialized": "data"}
        }


class TestSerializeDictEdgeCases:
    """Test edge cases for dict serialization"""
    
    def test_dict_with_numeric_string_keys(self):
        """Test dict with numeric string keys"""
        obj = {"1": "one", "2": "two"}
        result = serialize(obj)
        assert result == {"1": "one", "2": "two"}
    
    def test_dict_with_special_char_keys(self):
        """Test dict with special characters in keys"""
        obj = {"key-1": "value1", "key_2": "value2", "key.3": "value3"}
        result = serialize(obj)
        assert result == {"key-1": "value1", "key_2": "value2", "key.3": "value3"}
    
    def test_dict_with_unicode_keys(self):
        """Test dict with unicode keys"""
        obj = {"café": "coffee", "naïve": "simple"}
        result = serialize(obj)
        assert result == {"café": "coffee", "naïve": "simple"}
    
    def test_dict_with_unicode_values(self):
        """Test dict with unicode values"""
        obj = {"greeting": "Hello 世界", "emoji": "🎉"}
        result = serialize(obj)
        assert result == {"greeting": "Hello 世界", "emoji": "🎉"}
    
    def test_dict_with_all_none_values(self):
        """Test dict where all values are None"""
        obj = {"key1": None, "key2": None, "key3": None}
        result = serialize(obj)
        # All None values should be preserved as None
        assert result == {"key1": None, "key2": None, "key3": None}
    
    def test_dict_with_mixed_none_and_values(self):
        """Test dict with alternating None and actual values"""
        obj = {
            "key1": "value1",
            "key2": None,
            "key3": "value3",
            "key4": None,
            "key5": "value5"
        }
        result = serialize(obj)
        # None values should be preserved as None
        assert result == {"key1": "value1", "key2": None, "key3": "value3", "key4": None, "key5": "value5"}
    
    def test_dict_preserves_key_order(self):
        """Test that dict key order is preserved (Python 3.7+)"""
        obj = {"z": 1, "a": 2, "m": 3}
        result = serialize(obj)
        assert list(result.keys()) == ["z", "a", "m"]
    
    def test_dict_with_zero_values(self):
        """Test dict with zero values (should not be excluded)"""
        obj = {"count": 0, "price": 0.0, "active": False}
        result = serialize(obj)
        assert result == {"count": 0, "price": 0.0, "active": False}
    
    def test_dict_with_empty_string_values(self):
        """Test dict with empty string values (should not be excluded)"""
        obj = {"name": "", "description": ""}
        result = serialize(obj)
        assert result == {"name": "", "description": ""}
    
    def test_very_large_dict(self):
        """Test serialization of a large dict"""
        obj = {f"key{i}": f"value{i}" for i in range(1000)}
        result = serialize(obj)
        assert len(result) == 1000
        assert result["key500"] == "value500"


class TestSerializeDictComplex:
    """Test complex nested scenarios"""
    
    def test_dict_with_complex_nested_structure(self):
        """Test dict with complex nested structure mixing types"""
        dt = datetime(2023, 1, 15, 10, 30, 45)
        obj = {
            "metadata": {
                "created": dt,
                "author": "test_user",
                "tags": ["tag1", "tag2"]
            },
            "data": {
                "items": [
                    {"id": 1, "value": "first"},
                    {"id": 2, "value": None}
                ],
                "count": 2
            },
            "settings": {
                "enabled": True,
                "threshold": 0.5
            }
        }
        result = serialize(obj)
        
        assert result["metadata"]["created"] == dt.isoformat() + "Z"
        assert result["metadata"]["author"] == "test_user"
        assert result["metadata"]["tags"] == ["tag1", "tag2"]
        assert result["data"]["items"] == [
            {"id": 1, "value": "first"},
            {"id": 2, "value": None}  # None value preserved as None
        ]
        assert result["data"]["count"] == 2
        assert result["settings"]["enabled"] is True
        assert result["settings"]["threshold"] == 0.5
    
    def test_dict_circular_reference_prevention(self):
        """Test that dict doesn't cause infinite recursion with nested structure"""
        # Create a deeply nested but finite structure
        obj = {"level": 1}
        current = obj
        for i in range(2, 11):
            current["nested"] = {"level": i}
            current = current["nested"]
        
        result = serialize(obj)
        assert result["level"] == 1
        assert result["nested"]["level"] == 2
