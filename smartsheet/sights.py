# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2017 Smartsheet.com, Inc.
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
from typing import Optional, Union

from .util import fresh_operation
from .models import Error, Result, Sight, SightPublish, TokenPaginatedResult


class Sights:

    """Class for handling Sights operations."""

    def __init__(self, smartsheet_obj):
        """Init Sights with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_sights(
        self,
        last_key: Optional[str] = None,
        max_items: Optional[int] = None,
    ) -> Union[TokenPaginatedResult[Sight], Error]:
        """Get the list of all Sights the User has access to, in alphabetical
        order, by name.

        Args:
            last_key (str, optional): Pagination cursor for next page.
            max_items (int, optional): Maximum items per page. Must be a positive integer.

        Returns:
            TokenPaginatedResult[Sight]: The result of the operation.

        Raises:
            ValueError: If max_items <= 0.
        """
        if max_items is not None and max_items <= 0:
            raise ValueError("max_items must be a positive integer")

        _op = fresh_operation("list_sights")
        _op["method"] = "GET"
        _op["path"] = "/sights"
        _op["query_params"]["lastKey"] = last_key
        _op["query_params"]["maxItems"] = max_items

        expected = ["TokenPaginatedResult", "Sight"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_sight(self, sight_id, level=None, include=None) -> Union[Sight, Error]:
        """Get the specified Sight.

        Args:
            sight_id (int): Sight ID
            level (int): compatibility level
            include (list[str]): optional include parameters

        Returns:
            Union[Sight, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_sight")
        _op["method"] = "GET"
        _op["path"] = "/sights/" + str(sight_id)
        _op["query_params"]["include"] = include
        _op["query_params"]["level"] = level

        expected = "Sight"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_sight(self, sight_id, sight_obj) -> Union[Result[Sight], Error]:
        """Updates the specified Sight.

        Args:
            sight_id (int): Sight ID
            sight_obj (Sight): Sight object.

        Returns:
            Union[Result[Sight], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("update_sight")
        _op["method"] = "PUT"
        _op["path"] = "/sights/" + str(sight_id)
        _op["json"] = sight_obj

        expected = ["Result", "Sight"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_sight(self, sight_id) -> Union[Result[None], Error]:
        """Delete the specified Sight.

        Args:
            sight_id (int): Sight ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("delete_sight")
        _op["method"] = "DELETE"
        _op["path"] = "/sights/" + str(sight_id)

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def copy_sight(self, sight_id, container_destination_obj) -> Union[Result[Sight], Error]:
        """Creates a copy of the specified Sight

        Args:
            sight_id (int): Sight ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Union[Result[Sight], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("copy_sight")
        _op["method"] = "POST"
        _op["path"] = "/sights/" + str(sight_id) + "/copy"
        _op["json"] = container_destination_obj

        expected = ["Result", "Sight"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def move_sight(self, sight_id, container_destination_obj) -> Union[Result[Sight], Error]:
        """Creates a copy of the specified Sight

        Args:
            sight_id (int): Sight ID
            container_destination_obj
                (ContainerDestination): Container Destination object.

        Returns:
            Union[Result[Sight], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("move_sight")
        _op["method"] = "POST"
        _op["path"] = "/sights/" + str(sight_id) + "/move"
        _op["json"] = container_destination_obj

        expected = ["Result", "Sight"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_publish_status(self, sight_id) -> Union[SightPublish, Error]:
        """Get the Publish status of the Sight.

        Get the status of the Publish settings of the Sight,
        including URLs of any enabled publishings.

        Args:
            sight_id (int): Sight ID

        Returns:
            Union[Sight, Error]: The result of the operation, or an Error object if the request fails.Publish
        """
        _op = fresh_operation("get_publish_status")
        _op["method"] = "GET"
        _op["path"] = "/sights/" + str(sight_id) + "/publish"

        expected = "SightPublish"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def set_publish_status(self, sight_id, sight_publish_obj) -> Union[Result[SightPublish], Error]:
        """Set the publish status of the Sight and returns the new status,
        including the URLs of any enabled publishings.

        Args:
            sight_id (int): Sight ID
            sight_publish_obj (SightPublish): SightPublish object.

        Returns:
            Union[Result[SightPublish], Error]: The result of the operation, or an Error object if the request fails.
        """
        attributes = ["read_only_full_enabled", "read_only_full_accessible_by"]

        fetch_first = False
        # check for incompleteness, fill in from current status if necessary
        for attribute in attributes:
            val = getattr(sight_publish_obj, attribute, None)
            if val is None:
                fetch_first = True
                break

        if fetch_first:
            current_status = self.get_publish_status(sight_id).to_dict()
            current_status.update(sight_publish_obj.to_dict())
            sight_publish_obj = self._base.models.SightPublish(current_status)

        _op = fresh_operation("set_publish_status")
        _op["method"] = "PUT"
        _op["path"] = "/sights/" + str(sight_id) + "/publish"
        _op["json"] = sight_publish_obj

        expected = ["Result", "SightPublish"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
