# pylint: disable=C0111,R0902,R0913
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
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

from __future__ import absolute_import

from typing import Union, List

import logging

from .util import fresh_operation
from .models import Error, Favorite, IndexResult, Result
from .models.enums import FavoriteType


class Favorites:

    """Class for handling Favorites operations."""

    def __init__(self, smartsheet_obj):
        """Init Favorites with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_favorites(self, favorite_obj) -> Union[Result[Union[Favorite, List[Favorite]]], Error]:
        """Add one or more items to the user's list of Favorite items.

        Adds one or more items to the user's list of Favorite
        items. This operation supports both single-object and bulk
        semantics. If called with a single Favorite object, and that
        favorite already exists, error code 1129 will be returned. If
        called with an array of Favorite objects, any objects specified in
        the array that are already marked as favorites will be ignored and
        ommitted from the response.

        Args:
            favorite_obj (list[Favorite]): Array of one or
                more Favorite objects

        Returns:
            Union[Result[Union[Favorite, List[Favorite]]], Error]: The result of the operation - either a list or a
            single object, or an Error object if the request fails.
        """
        _op = fresh_operation("add_favorites")
        _op["method"] = "POST"
        _op["path"] = "/favorites"
        _op["json"] = favorite_obj

        expected = ["Result", "Favorite"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_favorites(self, page_size=None, page=None, include_all=None) -> Union[IndexResult[Favorite], Error]:
        """Get a list of all the user's Favorite items.

        Args:
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            Union[IndexResult[Favorite], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_favorites")
        _op["method"] = "GET"
        _op["path"] = "/favorites"
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["includeAll"] = include_all

        expected = ["IndexResult", "Favorite"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_favorites(self, favorite_type: FavoriteType, object_ids: list[int]) -> Union[Result[None], Error]:
        """Delete one or more of Favorite objects of the specified type.

        Args:
            favorite_type FavoriteType: The favorite type enum value.
            object_ids (list[int]): a comma-separated list
                of object IDs representing the items to work on.

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """

        _op = fresh_operation("remove_favorites")
        _op["method"] = "DELETE"
        _op["path"] = "/favorites/" + favorite_type
        _op["query_params"]["objectIds"] = object_ids

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def is_favorite(self, favorite_type: FavoriteType, favorite_id: int, include=None) -> Union[Favorite, Error]:
        """Check whether an item has been tagged as a favorite for the current user.

        Args:
            favorite_type FavoriteType: The favorite type enum value.
            favorite_id (int): ID of the favorite being accessed.
            include (str): A comma-separated list of optional elements to
                include in the response. Valid values: "directId", "name".

        Returns:
            Union[Favorite, Error]: The Favorite object if the item is favorited,
            or an Error object if the request fails or the item is not favorited.
        """

        _op = fresh_operation("is_favorite")
        _op["method"] = "GET"
        _op["path"] = "/favorites/" + favorite_type + "/" + str(favorite_id)
        if include is not None:
            _op["query_params"]["include"] = include

        expected = "Favorite"

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
