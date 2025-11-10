import json
import uuid
from urllib.parse import urlparse, parse_qs

import pytest
from smartsheet.models.enums import AssetType, AccessLevel, ShareScope, ShareType
from smartsheet.models import AssetShare, AssetSharesPaginatedResult, Error
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


# Test constants
TEST_ASSET_ID = "AAAMCmYGFOeE"
TEST_SHARE_ID = "AAABbbbCccDdd"
TEST_ASSET_TYPE = AssetType.SHEET
TEST_EMAIL = "test.email@smartsheet.com"
TEST_USER_ID = "9876543210"
TEST_GROUP_ID = "1234567890"
TEST_NAME = "Example Name"
TEST_SHARE_TYPE = ShareType.USER
TEST_ACCESS_LEVEL = AccessLevel.ADMIN
TEST_SCOPE = ShareScope.ITEM
TEST_MAX_ITEMS = 100
TEST_LAST_KEY = "test_last_key"
TEST_LAST_KEY_RESPONSE = "abcDefGhIjKlMnOpQrStUvWxYz"
TEST_SUCCESS_MESSAGE = "SUCCESS"
TEST_SUCCESS_RESULT_CODE = 0
TEST_SEND_EMAIL = False
TEST_CC_ME = True
TEST_MESSAGE = "Test message"
TEST_SUBJECT = "Test subject"


def assert_share_properties(share, include_name=True):
    """Helper function to assert common share properties."""
    assert isinstance(share, AssetShare)
    assert share.id == TEST_ASSET_ID
    assert share.email == TEST_EMAIL
    assert share.user_id == TEST_USER_ID
    assert share.group_id == TEST_GROUP_ID
    if include_name:
        assert share.name == TEST_NAME
    else:
        assert share.name is None
    assert share.type == TEST_SHARE_TYPE
    assert share.access_level == TEST_ACCESS_LEVEL
    assert share.scope == TEST_SCOPE


@pytest.fixture(name="test_share")
def test_share_fixture():
    """Pytest fixture to create a test AssetShare object."""
    return AssetShare({
        "email": TEST_EMAIL,
        "access_level": TEST_ACCESS_LEVEL,
        "cc_me": TEST_CC_ME,
        "message": TEST_MESSAGE,
        "subject": TEST_SUBJECT
    })


def test_list_asset_shares_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/list-asset-shares/all-response-body-properties", request_id
    )

    client.Sharing.list_asset_shares(
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        max_items=TEST_MAX_ITEMS,
        last_key=TEST_LAST_KEY,
        sharing_include=TEST_SCOPE,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "assetType": [TEST_ASSET_TYPE.value],
        "assetId": [TEST_ASSET_ID],
        "maxItems": [str(TEST_MAX_ITEMS)],
        "lastKey": [TEST_LAST_KEY],
        "sharingInclude": [TEST_SCOPE.name],
    }


def test_list_asset_shares_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/list-asset-shares/all-response-body-properties", request_id
    )

    response = client.Sharing.list_asset_shares(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID
    )

    assert isinstance(response, AssetSharesPaginatedResult)

    assert response.last_key == TEST_LAST_KEY_RESPONSE
    assert len(response.items) == 1

    share = response.items[0]
    assert isinstance(share, AssetShare)

    assert share.id == TEST_ASSET_ID
    assert share.email == TEST_EMAIL
    assert share.user_id == TEST_USER_ID
    assert share.group_id == TEST_GROUP_ID
    assert share.name == TEST_NAME
    assert share.type == TEST_SHARE_TYPE
    assert share.access_level == TEST_ACCESS_LEVEL
    assert share.scope == TEST_SCOPE


def test_list_asset_shares_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/list-asset-shares/required-response-body-properties", request_id
    )

    response = client.Sharing.list_asset_shares(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID
    )

    assert isinstance(response, AssetSharesPaginatedResult)

    assert response.last_key is None
    assert len(response.items) == 1

    share = response.items[0]
    assert isinstance(share, AssetShare)

    assert share.id == TEST_ASSET_ID
    assert share.email == TEST_EMAIL
    assert share.user_id == TEST_USER_ID
    assert share.group_id == TEST_GROUP_ID
    assert share.name is None
    assert share.type == TEST_SHARE_TYPE
    assert share.access_level == TEST_ACCESS_LEVEL
    assert share.scope == TEST_SCOPE

def test_list_asset_shares_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sharing.list_asset_shares(
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        max_items=TEST_MAX_ITEMS,
        last_key=TEST_LAST_KEY,
        sharing_include=TEST_SCOPE,
    )

    assert isinstance(response, Error)

def test_list_asset_shares_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sharing.list_asset_shares(
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        max_items=TEST_MAX_ITEMS,
        last_key=TEST_LAST_KEY,
        sharing_include=TEST_SCOPE,
    )

    assert isinstance(response, Error)

def test_get_asset_share_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/get-asset-share/all-response-body-properties", request_id
    )

    client.Sharing.get_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/shares/{TEST_SHARE_ID}'
    query = parse_qs(url.query)
    assert query == {
        "assetType": [TEST_ASSET_TYPE.value],
        "assetId": [TEST_ASSET_ID],
    }

def test_get_asset_share_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/get-asset-share/all-response-body-properties", request_id
    )

    response = client.Sharing.get_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert_share_properties(response, include_name=True)


def test_get_asset_share_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/get-asset-share/required-response-body-properties", request_id
    )

    response = client.Sharing.get_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert_share_properties(response, include_name=False)

def test_get_asset_share_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sharing.get_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert isinstance(response, Error)

def test_get_asset_share_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sharing.get_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert isinstance(response, Error)

def test_share_asset_generated_url_is_correct(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/share-asset/all-response-body-properties", request_id
    )

    client.Sharing.share_asset(
        share_obj=test_share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == '/2.0/shares'
    query = parse_qs(url.query)
    assert query == {
        "assetType": [TEST_ASSET_TYPE.value],
        "assetId": [TEST_ASSET_ID],
        "sendEmail": [str(TEST_SEND_EMAIL)]
    }

def test_share_asset_all_response_properties(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/share-asset/all-response-body-properties", request_id
    )

    response = client.Sharing.share_asset(
        share_obj=test_share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    assert response.result is not None
    assert isinstance(response.result, list)
    assert len(response.result) == 1

    share_result = response.result[0]
    assert_share_properties(share_result, include_name=True)

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == {
        "accessLevel": TEST_ACCESS_LEVEL.name,
        "email": TEST_EMAIL,
        "ccMe": TEST_CC_ME,
        "message": TEST_MESSAGE,
        "subject": TEST_SUBJECT
    }


def test_share_multiple_assets_all_response_properties(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/share-asset/all-response-body-properties", request_id
    )

    shares = [test_share]

    response = client.Sharing.share_asset(
        share_obj=shares,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    assert response.result is not None
    assert isinstance(response.result, list)
    assert len(response.result) == 1

    share_result = response.result[0]
    assert_share_properties(share_result, include_name=True)

    wiremock_request = get_wiremock_request(request_id)
    body = json.loads(wiremock_request["body"])
    assert body == [{
        "accessLevel": TEST_ACCESS_LEVEL.name,
        "email": TEST_EMAIL,
        "ccMe": TEST_CC_ME,
        "message": TEST_MESSAGE,
        "subject": TEST_SUBJECT
    }]



def test_share_asset_required_response_properties(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/share-asset/required-response-body-properties", request_id
    )

    response = client.Sharing.share_asset(
        share_obj=test_share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    assert response.result is not None
    assert isinstance(response.result, list)
    assert len(response.result) == 1

    share_result = response.result[0]
    assert_share_properties(share_result, include_name=False)

def test_share_asset_error_4xx(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sharing.share_asset(
        share_obj=test_share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    assert isinstance(response, Error)

def test_share_asset_error_5xx(test_share):
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sharing.share_asset(
        share_obj=test_share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        send_email=False,
    )

    assert isinstance(response, Error)

def test_update_asset_share_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/update-asset-share/all-response-body-properties", request_id
    )

    share = AssetShare({"access_level": TEST_ACCESS_LEVEL})

    client.Sharing.update_asset_share(
        share_obj=share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        share_id=TEST_SHARE_ID,
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/shares/{TEST_SHARE_ID}'
    query = parse_qs(url.query)
    assert query == {
        "assetType": [TEST_ASSET_TYPE.value],
        "assetId": [TEST_ASSET_ID],
    }

def test_update_asset_share_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/update-asset-share/all-response-body-properties", request_id
    )

    share = AssetShare({"access_level": TEST_ACCESS_LEVEL})

    response = client.Sharing.update_asset_share(
        share_obj=share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        share_id=TEST_SHARE_ID,
    )

    # Update returns the AssetShare object directly, not wrapped in result
    assert_share_properties(response, include_name=True)


def test_update_asset_share_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/update-asset-share/required-response-body-properties", request_id
    )

    share = AssetShare({"access_level": TEST_ACCESS_LEVEL})

    response = client.Sharing.update_asset_share(
        share_obj=share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        share_id=TEST_SHARE_ID,
    )

    # Update returns the AssetShare object directly, not wrapped in result
    assert_share_properties(response, include_name=False)

def test_update_asset_share_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    share = AssetShare({"access_level": TEST_ACCESS_LEVEL})

    response = client.Sharing.update_asset_share(
        share_obj=share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        share_id=TEST_SHARE_ID,
    )

    assert isinstance(response, Error)

def test_update_asset_share_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    share = AssetShare({"access_level": TEST_ACCESS_LEVEL})

    response = client.Sharing.update_asset_share(
        share_obj=share,
        asset_type=TEST_ASSET_TYPE,
        asset_id=TEST_ASSET_ID,
        share_id=TEST_SHARE_ID,
    )

    assert isinstance(response, Error)

def test_delete_asset_share_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/delete-asset-share/all-response-body-properties", request_id
    )

    client.Sharing.delete_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    assert url.path == f'/2.0/shares/{TEST_SHARE_ID}'
    query = parse_qs(url.query)
    assert query == {
        "assetType": [TEST_ASSET_TYPE.value],
        "assetId": [TEST_ASSET_ID],
    }

def test_delete_asset_share_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/sharing/delete-asset-share/all-response-body-properties", request_id
    )

    response = client.Sharing.delete_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert response.message == TEST_SUCCESS_MESSAGE
    assert response.result_code == TEST_SUCCESS_RESULT_CODE

def test_delete_asset_share_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Sharing.delete_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert isinstance(response, Error)

def test_delete_asset_share_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Sharing.delete_asset_share(
        asset_type=TEST_ASSET_TYPE, asset_id=TEST_ASSET_ID, share_id=TEST_SHARE_ID
    )

    assert isinstance(response, Error)
