# pylint: disable=missing-function-docstring
import pytest

from smartsheet.smartsheet_integration_source_validator import (
    is_valid_format,
    SmartsheetIntegrationSourceType,
)
from smartsheet.exceptions import SmartsheetException


def test_valid_formats_minimum_and_with_org():
    assert is_valid_format("AI,,Integrator") is True
    assert is_valid_format("APPLICATION,Org Name,Integrator Name") is True
    assert is_valid_format("SCRIPT,Acme Inc,MyBot") is True


def test_invalid_when_null():
    with pytest.raises(SmartsheetException) as exc:
        is_valid_format(None)  # type: ignore[arg-type]
    assert "cannot be null" in str(exc.value)


def test_invalid_when_wrong_number_of_parts():
    for bad in ["AI,OnlyTwo", "AI,Org,Name,Extra", "AI"]:
        with pytest.raises(SmartsheetException) as exc:
            is_valid_format(bad)
        assert "Invalid smartsheet integration source format" in str(exc.value)


def test_invalid_when_type_not_allowed():
    with pytest.raises(SmartsheetException) as exc:
        is_valid_format("NOT_A_TYPE,Org,Integrator")
    assert "The integration type has to be one of the following" in str(exc.value)
    # ensure enum contains expected members
    names = {t.name for t in SmartsheetIntegrationSourceType}
    assert {"AI", "SCRIPT", "APPLICATION"}.issubset(names)


def test_invalid_when_integrator_missing():
    with pytest.raises(SmartsheetException) as exc:
        is_valid_format("AI,Org,")
    assert "integrator name cannot be empty" in str(exc.value)
