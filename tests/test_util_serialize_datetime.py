"""Regression tests for ISO 8601 datetime serialization."""

from datetime import date, datetime, timedelta, timezone

import pytest
from dateutil.parser import isoparse

from smartsheet.models import Sheet
from smartsheet.util import serialize


@pytest.mark.parametrize("offset_minutes", [0, 330, -420])
@pytest.mark.parametrize("container", ["direct", "dict", "sheet"])
def test_serialize_aware_datetime_preserves_offset(offset_minutes, container):
    """Aware datetimes retain one valid timezone designator in every container."""
    value = datetime(
        2026, 10, 28, 12, 30, 45, 123456,
        tzinfo=timezone(timedelta(minutes=offset_minutes)),
    )
    if container == "direct":
        result = serialize(value)
    elif container == "dict":
        result = serialize({"nested": {"timestamp": value}})["nested"]["timestamp"]
    else:
        result = Sheet({"modifiedAt": value}).to_dict()["modifiedAt"]
    assert result == value.isoformat()
    assert isoparse(result) == value


@pytest.mark.parametrize("container", ["direct", "dict", "sheet"])
def test_serialize_naive_datetime_keeps_utc_suffix(container):
    """Preserve the existing convention for datetimes without a timezone."""
    value = datetime(2026, 10, 28, 12, 30, 45)
    if container == "direct":
        result = serialize(value)
    elif container == "dict":
        result = serialize({"timestamp": value})["timestamp"]
    else:
        result = Sheet({"modifiedAt": value}).to_dict()["modifiedAt"]
    assert result == "2026-10-28T12:30:45Z"


def test_serialize_date_keeps_date_only():
    """A date does not acquire a time or timezone component."""
    assert serialize(date(2026, 10, 28)) == "2026-10-28"
