# pylint: disable=C0111
from __future__ import annotations

from enum import Enum

from .exceptions import SmartsheetException
from .models.enums.smartsheet_integration_source_type import SmartsheetIntegrationSourceType

# Documentation link for error messages
DOCUMENTATION_LINK = "https://developers.smartsheet.com/api/smartsheet/guides/basics/http-and-rest#http-headers"

def is_valid_format(input_value: str) -> bool:
    """
    Validates a smartsheet integration source string in the format:
      type, organisation name, integrator name

    - type: must be one of the enum values
    - organisation name: optional (can be empty)
    - integrator name: non-empty
    """
    if input_value is None:
        raise SmartsheetException("Smartsheet integration source cannot be null")

    parts = input_value.split(",", -1)  # -1 keeps empty slots
    if len(parts) != 3:
        raise SmartsheetException(
            "Invalid smartsheet integration source format. "
            f"Expected format: 'TYPE,ORGANIZATION,INTEGRATOR. {DOCUMENTATION_LINK}"
        )

    integration_type = parts[0]
    integrator_name = parts[2]

    if not _is_valid_type(integration_type):
        allowed = [t.name for t in SmartsheetIntegrationSourceType]
        raise SmartsheetException(
            "Invalid smartsheet integration source format. "
            f"The integration type has to be one of the following: {allowed}. "
            f"Invalid integration type: {integration_type} {DOCUMENTATION_LINK}"
        )

    if integrator_name == "":
        raise SmartsheetException(
            "Invalid smartsheet integration source format. "
            "The integrator name cannot be empty."
        )

    return True


def _is_valid_type(integration_type_value: str | None) -> bool:
    if integration_type_value is None or integration_type_value == "":
        return False
    for source_type in SmartsheetIntegrationSourceType:
        if source_type.name.lower() == integration_type_value.lower():
            return True
    return False
