import json
import uuid
from urllib.parse import urlparse

from smartsheet.models import (
    Error,
    ReportDefinition,
    ReportFilterExpression,
    ReportGroupingCriterion,
    ReportSummarizingCriterion,
    ReportSortingCriterion,
)
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


# Test constants
TEST_REPORT_ID = 4583173393803140
TEST_SUCCESS_MESSAGE = "SUCCESS"
TEST_RESULT_CODE = 0


def test_update_report_definition_generated_url_is_correct():
    """Test that the URL is correctly generated for PUT /reports/{id}/definition."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    report_definition = ReportDefinition({
        "filters": {
            "operator": "AND",
            "criteria": []
        }
    })

    client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/definition'
    assert wiremock_request["method"] == "PUT"


def test_update_report_definition_request_body_with_nested_filters():
    """Test that request body is correctly serialized with nested filter criteria."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    # Create a complex filter expression with nested criteria to test circular marshalling
    filter_expression = ReportFilterExpression({
        "operator": "OR",
        "nestedCriteria": [
            {
                "operator": "AND",
                "nestedCriteria": [],
                "criteria": [
                    {
                        "column": {"title": "Price", "type": "TEXT_NUMBER"},
                        "operator": "GREATER_THAN",
                        "values": ["11"]
                    },
                    {
                        "column": {"primary": True},
                        "operator": "CONTAINS",
                        "values": ["PROJ-1"]
                    }
                ]
            },
            {
                "operator": "AND",
                "nestedCriteria": [],
                "criteria": [
                    {
                        "column": {"title": "Quantity", "type": "TEXT_NUMBER"},
                        "operator": "LESS_THAN",
                        "values": ["12"]
                    },
                    {
                        "column": {"title": "Sold Out", "type": "CHECKBOX"},
                        "operator": "IS_CHECKED",
                        "values": []
                    }
                ]
            }
        ],
        "criteria": []
    })

    grouping_criterion = ReportGroupingCriterion({
        "column": {"title": "Status", "type": "PICKLIST"},
        "sortingDirection": "ASCENDING",
    })

    summarizing_criterion = ReportSummarizingCriterion({
        "column": {"title": "Price", "type": "TEXT_NUMBER"},
        "aggregationType": "SUM",
    })

    sorting_criterion = ReportSortingCriterion({
        "column": {"title": "Date", "type": "DATE"},
        "sortingDirection": "DESCENDING",
    })

    report_definition = ReportDefinition()
    report_definition.filters = filter_expression
    report_definition.grouping_criteria = [grouping_criterion]
    report_definition.summarizing_criteria = [summarizing_criterion]
    report_definition.sorting_criteria = [sorting_criterion]

    client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    # Create expected request body structure matching serialization order
    # Note: Empty lists and nested criteria are omitted from serialization
    expected_body = {
        "filters": {
            "nestedCriteria": [
                {
                    "criteria": [
                        {
                            "column": {"title": "Price", "type": "TEXT_NUMBER"},
                            "operator": "GREATER_THAN",
                            "values": ["11"]
                        },
                        {
                            "column": {"primary": True},
                            "operator": "CONTAINS",
                            "values": ["PROJ-1"]
                        }
                    ],
                    "operator": "AND"
                },
                {
                    "criteria": [
                        {
                            "column": {"title": "Quantity", "type": "TEXT_NUMBER"},
                            "operator": "LESS_THAN",
                            "values": ["12"]
                        },
                        {
                            "column": {"title": "Sold Out", "type": "CHECKBOX"},
                            "operator": "IS_CHECKED"
                        }
                    ],
                    "operator": "AND"
                }
            ],
            "operator": "OR"
        },
        "groupingCriteria": [
            {
                "column": {"title": "Status", "type": "PICKLIST"},
                "sortingDirection": "ASCENDING"
            }
        ],
        "sortingCriteria": [
            {
                "column": {"title": "Date", "type": "DATE"},
                "sortingDirection": "DESCENDING"
            }
        ],
        "summarizingCriteria": [
            {
                "aggregationType": "SUM",
                "column": {"title": "Price", "type": "TEXT_NUMBER"}
            }
        ]
    }

    # Compare entire request body as dict
    assert actual_body == expected_body


def test_update_report_definition_partial_update_filters_only():
    """Test partial update with only filters property."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    filter_expression = ReportFilterExpression({
        "operator": "AND",
        "criteria": [
            {
                "column": {"title": "Status", "type": "PICKLIST"},
                "operator": "EQUAL",
                "values": ["Complete"]
            }
        ],
        "nestedCriteria": []
    })

    report_definition = ReportDefinition()
    report_definition.filters = filter_expression

    client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])

    # Verify only filters are in the request body
    assert "filters" in body
    assert body["filters"]["operator"] == "AND"
    assert len(body["filters"]["criteria"]) == 1


def test_update_report_definition_with_system_column():
    """Test filter with system column type and sheet name column."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    filter_expression = ReportFilterExpression({
        "operator": "AND",
        "criteria": [
            {
                "column": {"type": "TEXT_NUMBER", "sheetNameColumn": True},
                "operator": "CONTAINS",
                "values": ["Project"]
            },
            {
                "column": {"type": "DATETIME", "systemColumnType": "MODIFIED_DATE"},
                "operator": "LAST_N_DAYS",
                "values": ["7"]
            }
        ],
        "nestedCriteria": []
    })

    report_definition = ReportDefinition()
    report_definition.filters = filter_expression

    client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    # Create expected request body structure
    expected_body = {
        "filters": {
            "criteria": [
                {
                    "column": {"sheetNameColumn": True, "type": "TEXT_NUMBER"},
                    "operator": "CONTAINS",
                    "values": ["Project"]
                },
                {
                    "column": {"systemColumnType": "MODIFIED_DATE", "type": "DATETIME"},
                    "operator": "LAST_N_DAYS",
                    "values": ["7"]
                }
            ],
            "operator": "AND"
        }
    }

    # Compare entire request body as dict
    assert actual_body == expected_body


def test_update_report_definition_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    report_definition = ReportDefinition({
        "filters": {
            "operator": "AND",
            "criteria": []
        }
    })

    response = client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_RESULT_CODE


def test_update_report_definition_error_4xx():
    """Test 4xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    report_definition = ReportDefinition({
        "filters": {
            "operator": "AND",
            "criteria": []
        }
    })

    response = client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    assert isinstance(response, Error)


def test_update_report_definition_error_5xx():
    """Test 5xx error response handling."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    report_definition = ReportDefinition({
        "filters": {
            "operator": "AND",
            "criteria": []
        }
    })

    response = client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    assert isinstance(response, Error)


def test_update_report_definition_multiple_aggregation_types():
    """Test with multiple summarizing criteria using different aggregation types."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    summarizing_criteria = [
        ReportSummarizingCriterion({
            "column": {"title": "Price", "type": "TEXT_NUMBER"},
            "aggregationType": "SUM"
        }),
        ReportSummarizingCriterion({
            "column": {"title": "Quantity", "type": "TEXT_NUMBER"},
            "aggregationType": "AVG"
        }),
        ReportSummarizingCriterion({
            "column": {"title": "Date", "type": "DATE"},
            "aggregationType": "MIN"
        }),
        ReportSummarizingCriterion({
            "column": {"title": "Date", "type": "DATE"},
            "aggregationType": "MAX"
        }),
    ]

    report_definition = ReportDefinition()
    report_definition.summarizing_criteria = summarizing_criteria

    client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=report_definition,
    )

    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])

    # Create expected request body structure
    expected_body = {
        "summarizingCriteria": [
            {
                "column": {"title": "Price", "type": "TEXT_NUMBER"},
                "aggregationType": "SUM"
            },
            {
                "column": {"title": "Quantity", "type": "TEXT_NUMBER"},
                "aggregationType": "AVG"
            },
            {
                "column": {"title": "Date", "type": "DATE"},
                "aggregationType": "MIN"
            },
            {
                "column": {"title": "Date", "type": "DATE"},
                "aggregationType": "MAX"
            }
        ]
    }

    # Compare entire request body as dict
    assert actual_body == expected_body
