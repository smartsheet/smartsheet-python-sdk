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

        Requires either plan_id, or both asset_type and asset_id.

        Args:
            plan_id (int): The ID of the plan. Provide this or asset_type + asset_id.
            asset_type (AssetType): The type of the asset to resolve the plan from.
                Accepted values: AssetType.SHEET, AssetType.REPORT, AssetType.SIGHT (dashboard).
                Required together with asset_id when plan_id is not provided.
            asset_id (int): The ID of the asset to resolve the plan from.
                Required together with asset_type when plan_id is not provided.

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
