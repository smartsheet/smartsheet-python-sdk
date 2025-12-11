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
from typing import Union

from .util import fresh_operation
from .models import Error, IndexResult, Result, Webhook, WebhookSecret


class Webhooks:

    """Class for handling Webhooks operations."""

    def __init__(self, smartsheet_obj):
        """Init Webhooks with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def list_webhooks(self, page_size=None, page=None, include_all=None) -> Union[IndexResult[Webhook], Error]:
        """Get the list of all Webhooks the User has access to, in alphabetical
        order, by name.

        Args:
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).

        Returns:
            Union[IndexResult[Webhook], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_webhooks")
        _op["method"] = "GET"
        _op["path"] = "/webhooks"
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["includeAll"] = include_all

        expected = ["IndexResult", "Webhook"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_webhook(self, webhook_id) -> Union[Webhook, Error]:
        """Get the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Union[Webhook, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_webhook")
        _op["method"] = "GET"
        _op["path"] = "/webhooks/" + str(webhook_id)

        expected = "Webhook"

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def create_webhook(self, webhook_obj) -> Union[Result[Webhook], Error]:
        """Creates the specified Webhook.

        Args:
            webhook_obj (Webhook): Webhook object.

        Returns:
            Union[Result[Webhook], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("create_webhook")
        _op["method"] = "POST"
        _op["path"] = "/webhooks"
        _op["json"] = webhook_obj

        expected = ["Result", "Webhook"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_webhook(self, webhook_id, webhook_obj) -> Union[Result[Webhook], Error]:
        """Updates the specified Webhook.

        Args:
            webhook_id (int): Webhook ID
            webhook_obj (Webhook): Webhook object.

        Returns:
            Union[Result[Webhook], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("update_webhook")
        _op["method"] = "PUT"
        _op["path"] = "/webhooks/" + str(webhook_id)
        _op["json"] = webhook_obj

        expected = ["Result", "Webhook"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_webhook(self, webhook_id) -> Union[Result[None], Error]:
        """Delete the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("delete_webhook")
        _op["method"] = "DELETE"
        _op["path"] = "/webhooks/" + str(webhook_id)

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def reset_shared_secret(self, webhook_id) -> Union[Result[WebhookSecret], Error]:
        """Resets the shared secret for the specified Webhook.

        Args:
            webhook_id (int): Webhook ID

        Returns:
            Union[Result[WebhookSecret], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("reset_webhook")
        _op["method"] = "POST"
        _op["path"] = "/webhooks/" + str(webhook_id) + "/resetsharedsecret"

        expected = ["Result", "WebhookSecret"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
