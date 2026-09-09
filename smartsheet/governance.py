# pylint: disable=C0111,R0902,R0904,W0212,W0221
from __future__ import absolute_import

import logging

from .util import fresh_operation


class Governance:
    """Class for Governance-related operations."""

    def __init__(self, smartsheet_obj):
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def get_data_classification_settings(self, plan_id=None, asset_type=None, asset_id=None):
        # type: (int, str, int) -> object
        """Get the data classification settings for a plan.

        Requires either plan_id, or both asset_type and asset_id.

        Args:
            plan_id (int): The masked ID of the plan. Provide this or asset_type + asset_id.
            asset_type (str): The type of the asset to resolve the plan from.
                Accepted values: 'sheet', 'report', 'sight' (dashboard).
                Required together with asset_id when plan_id is not provided.
            asset_id (int): The masked ID of the asset to resolve the plan from.
                Required together with asset_type when plan_id is not provided.

        Returns:
            DataClassificationSettings
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
