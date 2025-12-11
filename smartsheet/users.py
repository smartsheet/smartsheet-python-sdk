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

from __future__ import absolute_import

from typing import Union, List

import logging
from datetime import datetime

from .util import fresh_operation
from .models import AlternateEmail, Error, IndexResult, Result, Sheet, TokenPaginatedResult, User, UserPlan, UserProfile
from .models.enums.seat_type import SeatType


class Users:

    """Class for handling Users operations."""

    def __init__(self, smartsheet_obj):
        """Init Users with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def add_alternate_email(self, user_id, list_of_alternate_emails) -> Union[Result[Union[AlternateEmail, List[AlternateEmail]]], Error]:
        """Add one or more alternate email addresses for the specified User

        Args:
            user_id (int): User ID
            list_of_alternate_emails (list[AlternateEmail]):
                An array of one or more AlternateEmail objects.

        Returns:
            Union[Result[List[AlternateEmail]], Error]: The result of the operation - either a list or a single object, or an Error object if the request fails.
        """
        _op = fresh_operation("add_alternate_email")
        _op["method"] = "POST"
        _op["path"] = "/users/" + str(user_id) + "/alternateemails"
        _op["json"] = list_of_alternate_emails

        expected = ["Result", "AlternateEmail"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def promote_alternate_email(self, user_id, alt_id) -> Union[Result[AlternateEmail], Error]:
        """Promote an email address to primary

        Args:
            user_id (int): User ID
            alt_id(int):  AlternateEmail ID to be promoted

        Returns:
            Union[Result[AlternateEmail], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("promote_alternate_email")
        _op["method"] = "POST"
        _op["path"] = (
            "/users/"
            + str(user_id)
            + "/alternateemails/"
            + str(alt_id)
            + "/makeprimary"
        )

        expected = ["Result", "AlternateEmail"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_user(self, user_obj, send_email=None) -> Union[Result[User], Error]:
        """Add a User to the organization.

        Args:
            user_obj (User): User object with the following attributes:

                email (required)

                admin (required)

                licensedSheetCreator (required)

                firstName (optional)

                lastName (optional)

                resourceViewer (optional)

            send_email (bool): Either true or false to indicate
            whether or not to notify the user by email. Default is false.

        Returns:
            Union[Result[User], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("add_user")
        _op["method"] = "POST"
        _op["path"] = "/users"
        _op["json"] = user_obj
        _op["query_params"]["sendEmail"] = send_email

        expected = ["Result", "User"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_alternate_email(self, user_id, alternate_email_id) -> Union[Result[None], Error]:
        """Deletes the specified alternate email address for the specified User.

        Args:
            user_id (int): User ID
            alternate_email_id (int): Alternate Email ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("delete_alternate_email")
        _op["method"] = "DELETE"
        _op["path"] = (
            "/users/" + str(user_id) + "/alternateemails/" +
            str(alternate_email_id)
        )

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_alternate_email(self, user_id, alternate_email_id) -> Union[AlternateEmail, Error]:
        """Get the specified Alternate Email

        Args:
            user_id (int): User ID
            alternate_email_id (int): Alternate Email ID

        Returns:
            Union[AlternateEmail, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_alternate_email")
        _op["method"] = "GET"
        _op["path"] = (
            "/users/" + str(user_id) + "/alternateemails/" +
            str(alternate_email_id)
        )

        expected = "AlternateEmail"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_current_user(self, include=None) -> Union[UserProfile, Error]:
        """Get the currently authenticated User.
        Returns:
            Union[UserProfile, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_current_user")
        _op["method"] = "GET"
        _op["path"] = "/users/me"
        _op["query_params"]["include"] = include

        expected = "UserProfile"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_user(self, user_id) -> Union[UserProfile, Error]:
        """Get the specified User.

        Args:
            user_id (int): User ID

        Returns:
            Union[UserProfile, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_user")
        _op["method"] = "GET"
        _op["path"] = "/users/" + str(user_id)

        expected = "UserProfile"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_alternate_emails(self, user_id) -> Union[IndexResult[AlternateEmail], Error]:
        """Get a list of the Alternate Emails for the specified User.

        Args:
            user_id (int): User ID

        Returns:
            Union[IndexResult[AlternateEmail], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_alternate_emails")
        _op["method"] = "GET"
        _op["path"] = "/users/" + str(user_id) + "/alternateemails"

        expected = ["IndexResult", "AlternateEmail"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_org_sheets(
        self, page_size=None, page=None, include_all=None, modified_since=None
    ) -> Union[IndexResult[Sheet], Error]:
        """Get a list of all Sheets owned by an organization.

        Get the list of all Sheets owned by the members of the
        account (organization).

        Args:
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).
            modified_since(datetime): list organization sheets modified since datetime

        Returns:
            Union[IndexResult[Sheet], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_org_sheets")
        _op["method"] = "GET"
        _op["path"] = "/users/sheets"
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["includeAll"] = include_all
        if isinstance(modified_since, datetime):
            _op["query_params"]["modifiedSince"] = modified_since.isoformat()

        expected = ["IndexResult", "Sheet"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_users(
        self, email=None, page_size=None, page=None, include_all=None, include=None,
        plan_id=None, seat_type=None
    ) -> Union[IndexResult[User], Error]:
        """Get the list of Users in the organization.

        Args:
            email (list[str]): Comma separated list of email
                addresses on which to filter the results.
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).
            include(list[str]): optional include parameter, only current
                accepted value is 'lastLogin'
            plan_id(int): optional plan_id parameter, returns users
                in the selected plan.
            seat_type(SeatType): optional seat_type parameter, filters users
                by their seat type.

        Returns:
            Union[IndexResult[User], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_users")
        _op["method"] = "GET"
        _op["path"] = "/users"
        _op["query_params"]["email"] = email
        _op["query_params"]["include"] = include
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["includeAll"] = include_all
        _op["query_params"]["planId"] = plan_id
        _op["query_params"]["seatType"] = seat_type

        expected = ["IndexResult", "User"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_user(
        self,
        user_id,
        transfer_to=None,
        transfer_sheets=False,
        remove_from_sharing=False,
    ) -> Union[Result[None], Error]:
        """Remove a user from an organization.

        Remove a User from an organization. User is transitioned to
        a free collaborator with read-only access to owned sheets, unless
        those are optionally transferred to another User.

        Args:
            user_id (int): User ID
            transfer_to (int): The ID of the User to
                transfer ownership to. If the User being removed owns
                groups, this value is required. Any groups owned by the User
                being removed will be transferred to the specified User. If
                the User owns sheets, _and_ **transferSheets** is `true`,
                the removed User's sheets will be transferred to the
                specified User.
            transfer_sheets (bool): If `true` and
                **transferTo** is specified, the removed User's sheets will
                be transferred. Otherwise, sheets will not be transferred.
                Defaults to `false`.
            remove_from_sharing (bool): Set to `true` to
                remove the user from sharing for all sheets/workspaces in
                the organization. If not specified, User will not be removed
                from sharing.

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("remove_user")
        _op["method"] = "DELETE"
        _op["path"] = "/users/" + str(user_id)
        _op["query_params"]["transferTo"] = transfer_to
        _op["query_params"]["transferSheets"] = transfer_sheets
        _op["query_params"]["removeFromSharing"] = remove_from_sharing

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def reactivate_user(self, user_id) -> Union[Result[None], Error]:
        """Reactivate the user associated with the current Smartsheet plan.

        Restores the user's access to Smartsheet, owned items, and shared items.

        Important: The user can only be reactivated if they have been deactivated
        for less than thirty (30) days.

        Optionally, with Enterprise Plan Manager (EPM) enabled, you can specify
        the ID of a user within your managed plan hierarchy.

        Args:
            user_id (int): User ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.

        Raises:
            ApiError: If the user cannot be reactivated. This occurs when:
                - The user's primary email address belongs to an ISP domain
                  (e.g., gmail.com, yahoo.com, outlook.com)
                - The user's primary email address is unassociated with the
                  current Smartsheet plan domain(s)
                - The user is not in the plan's organization
                - The user has been deactivated for more than 30 days

        Note:
            Requires System Admin permissions.
            This operation is unavailable for Smartsheet Gov.
        """
        _op = fresh_operation("reactivate_user")
        _op["method"] = "POST"
        _op["path"] = "/users/" + str(user_id) + "/reactivate"

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def deactivate_user(self, user_id) -> Union[Result[None], Error]:
        """Deactivate the user associated with the current Smartsheet plan.

        Blocks the user from using Smartsheet in any way. Deactivating a user
        does not affect their existing permissions on owned or shared items.
        Optionally, with Enterprise Plan Manager (EPM) enabled, you can deactivate
        a user from child organizations.

        Args:
            user_id (int): User ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.

        Raises:
            ApiError: If the user cannot be deactivated. This occurs when:
                - The user's primary email address belongs to an ISP domain
                  (e.g., gmail.com, yahoo.com, outlook.com)
                - The user's primary email address is unassociated with the
                  current Smartsheet plan domain(s)
                - The user is managed by an external source, such as an identity
                  provider (IdP) or directory integration (DI) provider
                  (e.g., Okta, Azure AD). Such users can only be deactivated
                  via the external source.

        Note:
            Requires System Admin permissions.
            This operation is unavailable for Smartsheet Gov.
        """
        _op = fresh_operation("deactivate_user")
        _op["method"] = "POST"
        _op["path"] = "/users/" + str(user_id) + "/deactivate"

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_user(self, user_id, user_obj) -> Union[Result[User], Error]:
        """Update the specified User.

        Args:
            user_id (int): User ID
            user_obj (User): User object with the following
                attributes:

        Returns:
            Union[Result[User], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("update_user")
        _op["method"] = "PUT"
        _op["path"] = "/users/" + str(user_id)
        _op["json"] = user_obj

        expected = ["Result", "User"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def upgrade_user(self, user_id, plan_id, seat_type) -> Union[Result[None], Error]:
        """Upgrades a user for a plan.

        Args:
            user_id (int): User ID
            plan_id (int): Plan ID
            seat_type (UpgradeSeatType): Seat type to upgrade to

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("upgrade_user")
        _op["method"] = "POST"
        _op["path"] = f"/users/{user_id}/plans/{plan_id}/upgrade"
        _op["json"] = {"seatType": seat_type}

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def downgrade_user(self, user_id, plan_id, seat_type) -> Union[Result[None], Error]:
        """Downgrades a user for a plan.

        Args:
            user_id (int): User ID
            plan_id (int): Plan ID
            seat_type (DowngradeSeatType): Seat type to downgrade to

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("downgrade_user")
        _op["method"] = "POST"
        _op["path"] = f"/users/{user_id}/plans/{plan_id}/downgrade"
        _op["json"] = {"seatType": seat_type}

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def list_user_plans(self, user_id, last_key=None, max_items=None) -> Union[TokenPaginatedResult[UserPlan], Error]:
        """List user's plans.
                Args:
                    user_id (int): User ID
                Returns:
                    Union[TokenPaginatedResult[UserPlan], Error]: The result of the operation, or an Error object if the request fails.
         """
        _op = fresh_operation("list_user_plans")
        _op["method"] = "GET"
        _op["path"] = f"/users/{user_id}/plans"
        _op["query_params"]["lastKey"] = last_key
        _op["query_params"]["maxItems"] = max_items

        expected = ["TokenPaginatedResult", "UserPlan"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_user_from_plan(self, user_id, plan_id) -> Union[Result[None], Error]:
        """Remove user from plan.
                        Args:
                            user_id (int): User ID
                            plan_id (int): Plan ID
                        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
                 """
        _op = fresh_operation("remove_user_from_plan")
        _op["method"] = "DELETE"
        _op["path"] = f"/users/{user_id}/plans/{plan_id}"

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_profile_image(self, user_id, file, file_type) -> Union[Result[User], Error]:
        """Uploads a profile image for the specified user.

        Args:
            user_id (int): user ID
            file (string): path to image file.
            file_type (string): content type of image file

        Returns:
            Union[Result[User], Error]: The result of the operation, or an Error object if the request fails.
        """
        if not all(val is not None for val in ["user_id", "file", "file_type"]):
            raise ValueError(
                ("One or more required values are missing from call to " + __name__)
            )

        return self._attach_profile_image(user_id, file, file_type)

    def _attach_profile_image(self, user_id, file, file_type) -> Union[Result[User], Error]:
        """Internal function used to load image"""

        _data = open(file, "rb").read()
        _op = fresh_operation("attach_profile_image")
        _op["method"] = "POST"
        _op["path"] = "/users/" + str(user_id) + "/profileimage"
        _op["headers"] = {
            "content-type": file_type,
            "content-disposition": 'attachment; filename="' + file + '"',
        }
        _op["form_data"] = _data

        expected = ["Result", "User"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
