import json
import uuid
from urllib.parse import urlparse, parse_qs

from smartsheet.models import Error
from tests.mock_api.favorites.common_test_constants import TEST_FAVORITE_ID, TEST_OBJECT_ID, TEST_FAVORITE_TYPE, TEST_DIRECT_ID, TEST_OBJECT_NAME
from tests.mock_api.mock_api_test_helper import (
    get_mock_api_client,
    get_wiremock_request,
)


def test_is_favorite_generated_url_is_correct():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/favorites/is-favorite/all-response-body-properties", request_id
    )

    client.Favorites.is_favorite(
        favorite_type=TEST_FAVORITE_TYPE,
        favorite_id=TEST_FAVORITE_ID,
        include="directId,name"
    )

    wiremock_request = get_wiremock_request(request_id)
    url = urlparse(wiremock_request["absoluteUrl"])
    query = parse_qs(url.query)
    assert query == {
        "include": ["directId,name"]
    }
    assert url.path == f'/2.0/favorites/{TEST_FAVORITE_TYPE.value}/{TEST_FAVORITE_ID}'

def test_is_favorite_all_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/favorites/is-favorite/all-response-body-properties", request_id
    )

    response = client.Favorites.is_favorite(
        favorite_type=TEST_FAVORITE_TYPE,
        favorite_id=TEST_FAVORITE_ID,
    )

    assert response.to_dict() == {
        "objectId": TEST_OBJECT_ID,
        "type": TEST_FAVORITE_TYPE,
        "directId": TEST_DIRECT_ID,
        "name": TEST_OBJECT_NAME
    }

def test_is_favorite_required_response_properties():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/favorites/is-favorite/required-response-body-properties", request_id
    )

    response = client.Favorites.is_favorite(
        favorite_type=TEST_FAVORITE_TYPE,
        favorite_id=TEST_FAVORITE_ID,
    )

    assert response.to_dict() == {
        "objectId": TEST_OBJECT_ID,
        "type": TEST_FAVORITE_TYPE
    }


def test_is_favorite_error_4xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/400-response", request_id
    )

    response = client.Favorites.is_favorite(
        favorite_type=TEST_FAVORITE_TYPE,
        favorite_id=TEST_FAVORITE_ID,
    )

    assert isinstance(response, Error)


def test_is_favorite_error_5xx():
    request_id = uuid.uuid4().hex
    client = get_mock_api_client(
        "/errors/500-response", request_id
    )

    response = client.Favorites.is_favorite(
        favorite_type=TEST_FAVORITE_TYPE,
        favorite_id=TEST_FAVORITE_ID,
    )

    assert isinstance(response, Error)
