from smartsheet.models import Sheet
from tests.mock_api.sheets.common_test_constants import TEST_SHEET_ID
from tests.mock_api.mock_api_test_helper import get_mock_api_client


def test_get_sheet_returns_data_classification_field():
    client = get_mock_api_client(
        "/sheets/get-sheet/data-classification", "test-request-id"
    )

    sheet = client.Sheets.get_sheet(sheet_id=TEST_SHEET_ID)

    assert isinstance(sheet, Sheet)
    assert sheet.to_dict() == {
        "id": 8244643726616452,
        "name": "Test Sheet",
        "dataClassification": "Confidential",
    }
