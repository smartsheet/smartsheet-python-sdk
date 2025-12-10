# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from typing import Union

from .util import fresh_operation
from .models import Error, AssetShare, AssetSharesPaginatedResult, Result
from .models.enums import ShareScope


class Sharing:
    """Class for handling Sharing operations."""

    def __init__(self, smartsheet_obj):
        """Init Sharing with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_asset_shares(self, asset_type, asset_id, max_items=None, last_key=None,
                          sharing_include: ShareScope = None) -> Union[AssetSharesPaginatedResult[AssetShare], Error]:
        """Get the list of all Users and Groups to whom the specified asset is
        shared, and their access level.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            max_items (int): The maximum number of items to
                return in the response.
            last_key (str): The token from a previous request that will allow this one
                to pick up where the previous one left off.
            sharing_include (ShareScope): Scope of share to include in response

        Returns:
            Union[AssetSharesPaginatedResult[AssetShare], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation('list_asset_shares')
        _op['method'] = 'GET'
        _op['path'] = '/shares'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['query_params']['maxItems'] = max_items
        _op['query_params']['lastKey'] = last_key
        _op['query_params']['sharingInclude'] = sharing_include.name if sharing_include else None

        expected = ['AssetSharesPaginatedResult', 'AssetShare']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_asset_share(self, asset_type, asset_id, share_id) -> Union[AssetShare, Error]:
        """Get a specific share for the specified asset.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID

        Returns:
            Union[AssetShare, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation('get_asset_share')
        _op['method'] = 'GET'
        _op['path'] = f'/shares/{share_id}'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id

        expected = 'AssetShare'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_asset(self, share_obj, asset_type, asset_id, send_email=None) -> Union[Result[AssetShare], Error]:
        """Share an asset with the specified Users and Groups.

        Args:
            share_obj (Share or list[Share]): Share object or list of Share objects.
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Union[Result[AssetShare], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation('share_asset')
        _op['method'] = 'POST'
        _op['path'] = '/shares'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj

        expected = ['Result', 'AssetShare']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_asset_share(self, share_obj, asset_type, asset_id, share_id) -> Union[AssetShare, Error]:
        """Update the access level of a User or Group for the specified asset.

        Args:
            share_obj (Share): Share object.
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID

        Returns:
            Union[AssetShare, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation('update_share')
        _op['method'] = 'PATCH'
        _op['path'] = f'/shares/{share_id}'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['json'] = share_obj

        expected = 'AssetShare'

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_asset_share(self, asset_type, asset_id, share_id) -> Union[Result[None], Error]:
        """Delete the specified Share.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation('delete_share')
        _op['method'] = 'DELETE'
        _op['path'] = f'/shares/{share_id}'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id

        expected = ['Result', None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
