# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

from typing import Optional, Union

import logging

from .models import DataClassificationSettings, Error
from .models.enums import AssetType
from .util import fresh_operation


class Governance:
    """Class for Governance-related operations."""

    def __init__(self, smartsheet_obj):
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_data_classification_settings(
        self,
        plan_id: Optional[int] = None,
        asset_type: Optional[AssetType] = None,
        asset_id: Optional[int] = None,
    ) -> Union[DataClassificationSettings, Error]:
        """Get the data classification settings for a plan.

        Provide either plan_id, or both asset_type and asset_id:

        - To get the settings for a plan, send plan_id.
        - When your request relates to a specific sheet, report, or dashboard,
          send asset_type and asset_id.

        Args:
            plan_id (int): The ID of the plan whose classification settings to return.
                Required unless asset_type and asset_id are provided. If all three
                are provided, asset_type and asset_id take precedence.
            asset_type (AssetType): The type of the asset: AssetType.SHEET,
                AssetType.REPORT, or AssetType.SIGHT (dashboard). Must be provided
                together with asset_id.
            asset_id (int): The ID of the sheet, report, or dashboard. Must be provided
                together with asset_type.

        Returns:
            Union[DataClassificationSettings, Error]: The data classification settings,
                or an Error object if the request fails.
        """
        _op = fresh_operation("get_data_classification_settings")
        _op["method"] = "GET"
        _op["path"] = "/governance/data-classification/settings"
        if plan_id is not None:
            _op["query_params"]["planId"] = plan_id
        if asset_type is not None:
            _op["query_params"]["assetType"] = asset_type
        if asset_id is not None:
            _op["query_params"]["assetId"] = asset_id
        expected = "DataClassificationSettings"
        prepped_request = self._base.prepare_request(_op)
        return self._base.request(prepped_request, expected, _op)
