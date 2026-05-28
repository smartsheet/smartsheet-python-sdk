import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import (
    Error,
    ReportDefinition,
    ReportFilterExpression,
    ReportGroupingCriterion,
    ReportSummarizingCriterion,
    ReportSortingCriterion,
    Result,
)
from tests.mock_api.reports.common_test_constants import TEST_SUCCESS_MESSAGE, TEST_RESULT_CODE
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


# ID matches WireMock update-report-definition fixtures, not common_test_constants.
TEST_REPORT_ID = 4583173393803140

EXPECTED_REQUEST_BODY = {
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


def _build_complex_report_definition():
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

    report_definition = ReportDefinition()
    report_definition.filters = filter_expression
    report_definition.grouping_criteria = [ReportGroupingCriterion({
        "column": {"title": "Status", "type": "PICKLIST"},
        "sortingDirection": "ASCENDING",
    })]
    report_definition.summarizing_criteria = [ReportSummarizingCriterion({
        "column": {"title": "Price", "type": "TEXT_NUMBER"},
        "aggregationType": "SUM",
    })]
    report_definition.sorting_criteria = [ReportSortingCriterion({
        "column": {"title": "Date", "type": "DATE"},
        "sortingDirection": "DESCENDING",
    })]
    return report_definition


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

    query = parse_qs(url.query)
    assert not query

    assert url.path == f'/2.0/reports/{TEST_REPORT_ID}/definition'
    assert wiremock_request["method"] == "PUT"


def test_update_report_definition_all_response_properties():
    """Test that all response properties are correctly deserialized."""
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/reports/update-report-definition/all-response-body-properties", request_id
    )

    response = client.Reports.update_report_definition(
        report_id=TEST_REPORT_ID,
        report_definition=_build_complex_report_definition(),
    )

    # Type safety checks
    assert isinstance(response, Result)

    # Request body assertion
    wiremock_request = get_wiremock_request(request_id)
    actual_body = json.loads(wiremock_request["body"])
    assert actual_body == EXPECTED_REQUEST_BODY

    # Response body assertion
    assert response.to_dict() == {
        "message": TEST_SUCCESS_MESSAGE,
        "resultCode": TEST_RESULT_CODE
    }


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
