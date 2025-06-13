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
from enum import Enum
from . import fresh_operation


class AssetType(str, Enum):
    """Defines the asset types supported by the Sharing API."""
    SHEET = 'sheet'
    REPORT = 'report'
    SIGHT = 'sight'
    WORKSPACE = 'workspace'
    COLLECTION = 'collection'
    FILE = 'file'


class Sharing:
    """Class for handling Sharing operations."""

    def __init__(self, smartsheet_obj):
        """Init Sharing with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_asset_shares(self, asset_type, asset_id, page_size=None, page=None, 
                         include_all=None, include_workspace_shares=False, 
                         access_api_level=0):
        """Get the list of all Users and Groups to whom the specified asset is
        shared, and their access level.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).
            include_workspace_shares(bool): Include Workspace shares
            access_api_level (int): Access API level

        Returns:
            IndexResult
        """
        _op = fresh_operation('list_asset_shares')
        _op['method'] = 'GET'
        _op['path'] = '/shares'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['query_params']['pageSize'] = page_size
        _op['query_params']['page'] = page
        _op['query_params']['includeAll'] = include_all
        _op['query_params']['accessApiLevel'] = access_api_level
        if include_workspace_shares:
            _op['query_params']['include'] = 'workspaceShares'

        expected = ['IndexResult', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_asset_share(self, asset_type, asset_id, share_id):
        """Get a specific share for the specified asset.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID

        Returns:
            Share
        """
        _op = fresh_operation('get_asset_share')
        _op['method'] = 'GET'
        _op['path'] = f'/shares/{share_id}'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id

        expected = 'Share'
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def share_asset(self, asset_type, asset_id, share_obj, send_email=None):
        """Share an asset with the specified Users and Groups.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_obj (Share or list[Share]): Share object or list of Share objects.
            send_email (bool): Either true or false to
                indicate whether or not to notify the user by email. Default
                is false.

        Returns:
            Result
        """
        _op = fresh_operation('share_asset')
        _op['method'] = 'POST'
        _op['path'] = '/shares'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['query_params']['sendEmail'] = send_email
        _op['json'] = share_obj

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_share(self, asset_type, asset_id, share_id, share_obj):
        """Update the access level of a User or Group for the specified asset.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID
            share_obj (Share): Share object.

        Returns:
            Result
        """
        _op = fresh_operation('update_share')
        _op['method'] = 'PATCH'
        _op['path'] = f'/shares/{share_id}'
        _op['query_params']['assetType'] = asset_type
        _op['query_params']['assetId'] = asset_id
        _op['json'] = share_obj

        expected = ['Result', 'Share']

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_share(self, asset_type, asset_id, share_id):
        """Delete the specified Share.

        Args:
            asset_type (AssetType): Type of asset (sheet, report, sight, workspace, etc.)
            asset_id (int): Asset ID
            share_id (str): Share ID

        Returns:
            Result
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