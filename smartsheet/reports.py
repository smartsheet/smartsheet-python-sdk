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

from typing import Union

import logging
import os.path
from datetime import datetime

from .util import fresh_operation
from .models import (
    CreateReportRequest,
    CreateReportResult,
    Error,
    DownloadedFile,
    IndexResult,
    Report,
    ReportColumn,
    ReportDefinition,
    ReportPublish,
    ReportScopeInclusion,
    Result,
)


class Reports:

    """Class for handling Reports operations."""

    def __init__(self, smartsheet_obj):
        """Init Reports with base Smartsheet object."""
        self._base = smartsheet_obj
        self._log = logging.getLogger(__name__)

    def create_report(self, create_report_request: CreateReportRequest) -> Union[Result[CreateReportResult], Error]:
        """Create a new report.

        Create a new report by specifying name, destination, scope, columns and definition.

        Args:
            create_report_request (CreateReportRequest): CreateReportRequest object containing:
                - name: Report name (required, 1-50 characters)
                - destination: Container destination (required)
                - columns: List of report columns (required, 1-400 items)
                - scope: List of scopes (required, 1-100 items)
                - report_definition: Report definition (optional)
                - is_summary_report: True for sheet summary report, False for row report (optional, default: False)

        Returns:
            Union[Result[CreateReportResult], Error]: Result object containing the CreateReportResult,
                or an Error object if the request fails.
        """
        _op = fresh_operation("create_report")
        _op["method"] = "POST"
        _op["path"] = "/reports"
        _op["json"] = create_report_request

        expected = ["Result", "CreateReportResult"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def delete_report(self, report_id) -> Union[Result[None], Error]:
        """Deletes a report based on the specified ID

        Args:
            report_id (int): Report ID

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("delete_report")
        _op["method"] = "DELETE"
        _op["path"] = "/reports/" + str(report_id)

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_report_columns(
        self, report_id: int, report_columns: list[ReportColumn]
    ) -> Union[Result[list[ReportColumn]], Error]:
        """Add columns to a report.

        Add columns to a report specified by a report ID. Note: all indexes of the columns
        must be equal.

        Args:
            report_id (int): Report ID
            report_columns (list[ReportColumn]): List of report columns to be added (1-400 items)

        Returns:
            Union[Result[list[ReportColumn]], Error]: Result object containing the list of
                ReportColumn objects that were added, or an Error object if the request fails.
        """
        _op = fresh_operation("add_report_columns")
        _op["method"] = "POST"
        _op["path"] = "/reports/" + str(report_id) + "/columns"
        _op["json"] = report_columns

        expected = ["Result", "ReportColumn"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_report(
        self, report_id, page_size=None, page=None, include=None, level=None
    ) -> Union[Report, Error]:
        """Get the specified Report, including one page of Rows.

        Get the specified Report, including one page of Rows, and
        optionally populated with Discussions, Attachments, and
        Source Sheets.

        Args:
            report_id (int): Report ID
            page_size (int): The maximum number of items to return per page.
            page (int): Which page to return.
            include (list[str]): A comma-separated list of
                optional elements to include in the response. Valid list values:
                attachments, discussions, format, objectValue, scope, source, sourceSheets.
            level (int): compatibility level

        Returns:
            Union[Report, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_report")
        _op["method"] = "GET"
        _op["path"] = "/reports/" + str(report_id)
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["include"] = include
        _op["query_params"]["level"] = level

        expected = "Report"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_report_as_csv(self, report_id, download_path, alternate_file_name=None) -> Union[DownloadedFile, Error]:
        """Get the specified Report as a CSV file.

        Args:
            report_id (int): Report ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            Union[DownloadedFile, Error]: The result of the operation, or an Error object if the request fails.
        """
        if not os.path.isdir(download_path):
            raise ValueError("download_path must be a directory.")

        _op = fresh_operation("get_report_as_csv")
        _op["method"] = "GET"
        _op["path"] = "/reports/" + str(report_id)
        _op["header_params"]["Accept"] = "text/csv"
        _op["dl_path"] = download_path

        expected = "DownloadedFile"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def get_report_as_excel(self, report_id, download_path, alternate_file_name=None) -> Union[DownloadedFile, Error]:
        """Get the specified Report as an Excel .xls document.

        Args:
            report_id (int): Report ID
            download_path (str): Directory path on local
                machine to save file.
            alternate_file_name (str): Filename to use
                instead of name suggested by Content-Disposition.

        Returns:
            Union[DownloadedFile, Error]: The result of the operation, or an Error object if the request fails.
        """
        if not os.path.isdir(download_path):
            raise ValueError("download_path must be a directory.")

        _op = fresh_operation("get_report_as_excel")
        _op["method"] = "GET"
        _op["path"] = "/reports/" + str(report_id)
        _op["header_params"]["Accept"] = "application/vnd.ms-excel"
        _op["dl_path"] = download_path

        expected = "DownloadedFile"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)
        if alternate_file_name is not None:
            response.filename = alternate_file_name

        response.save_to_file()
        return response

    def list_reports(
        self, page_size=None, page=None, include_all=None, modified_since=None
    ) -> Union[IndexResult[Report], Error]:
        """Get the list of all Reports accessible by the User.

        Get the list of all Reports that the User has access to, in
        alphabetical order by name.

        Args:
            page_size (int): The maximum number of items to
                return per page.
            page (int): Which page to return.
            include_all (bool): If true, include all results
                (i.e. do not paginate).
            modified_since(datetime): return reports modified after the specified modified_since

        Returns:
            Union[IndexResult[Report], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("list_reports")
        _op["method"] = "GET"
        _op["path"] = "/reports"
        _op["query_params"]["pageSize"] = page_size
        _op["query_params"]["page"] = page
        _op["query_params"]["includeAll"] = include_all
        if isinstance(modified_since, datetime):
            _op["query_params"]["modifiedSince"] = modified_since.isoformat()

        expected = ["IndexResult", "Report"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def send_report(self, report_id, sheet_email_obj) -> Union[Result[None], Error]:
        """Send the specified Report as a PDF attachment via email to the
        designated recipients.

        Args:
            report_id (int): Report ID
            sheet_email_obj (SheetEmail): SheetEmail object.

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("send_report")
        _op["method"] = "POST"
        _op["path"] = "/reports/" + str(report_id) + "/emails"
        _op["json"] = sheet_email_obj

        expected = ["Result", None]
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def get_publish_status(self, report_id) -> Union[ReportPublish, Error]:
        """Get the Publish status of the Report.

        Get the status of the Publish settings of the Report,
        including URLs of any enabled publishings.

        Args:
            report_id (int): Report ID

        Returns:
            Union[ReportPublish, Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("get_publish_status")
        _op["method"] = "GET"
        _op["path"] = "/reports/" + str(report_id) + "/publish"

        expected = "ReportPublish"
        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def set_publish_status(self, report_id, report_publish_obj) -> Union[Result[ReportPublish], Error]:
        """Set the publish status of the Report and returns the new status,
        including the URLs of any enabled publishings.

        Args:
            report_id (int): Report ID
            report_publish_obj (ReportPublish): ReportPublish
                object.

        Returns:
            Union[Result[ReportPublish], Error]: The result of the operation, or an Error object if the request fails.
        """
        attributes = ["read_only_full_enabled", "read_only_full_accessible_by"]

        fetch_first = False
        # check for incompleteness, fill in from current status if necessary
        for attribute in attributes:
            val = getattr(report_publish_obj, attribute, None)
            if val is None:
                fetch_first = True
                break

        if fetch_first:
            current_status = self.get_publish_status(report_id).to_dict()
            current_status.update(report_publish_obj.to_dict())
            report_publish_obj = self._base.models.ReportPublish(current_status)

        _op = fresh_operation("set_publish_status")
        _op["method"] = "PUT"
        _op["path"] = "/reports/" + str(report_id) + "/publish"
        _op["json"] = report_publish_obj

        expected = ["Result", "ReportPublish"]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def update_report_definition(self, report_id: int, report_definition: ReportDefinition) -> Union[Result[None], Error]:
        """Updates a report's definition.

        Update a Report's definition based on the specified ID.

        Note: This endpoint supports partial updates only on root level
        properties of the report definition, such as filters, groupingCriteria
        and summarizingCriteria. For example, you can update the report's
        filters without affecting its grouping criteria. However, nested
        properties within these objects, such as a specific filter or grouping
        criterion, cannot be updated individually and require a full replacement
        of the respective section.

        Args:
            report_id (int): Report ID
            report_definition (ReportDefinition): ReportDefinition object.
        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("update_report_definition")
        _op["method"] = "PUT"
        _op["path"] = "/reports/" + str(report_id) + "/definition"
        _op["json"] = report_definition

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def add_report_scope(self, report_id: int, scopes: list[ReportScopeInclusion]) -> Union[Result[None], Error]:
        """Add one or more scopes to the report.

        Args:
            report_id (int): Report ID
            scopes (list[ReportScopeInclusion]): List of scopes to add.

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("add_report_scope")
        _op["method"] = "POST"
        _op["path"] = "/reports/" + str(report_id) + "/scope"
        _op["json"] = scopes

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response

    def remove_report_scope(self, report_id: int, scopes: list[ReportScopeInclusion]) -> Union[Result[None], Error]:
        """Remove one or more scopes from the report.

        Args:
            report_id (int): Report ID
            scopes (list[ReportScopeInclusion]): List of scopes to remove.

        Returns:
            Union[Result[None], Error]: The result of the operation, or an Error object if the request fails.
        """
        _op = fresh_operation("remove_report_scope")
        _op["method"] = "DELETE"
        _op["path"] = "/reports/" + str(report_id) + "/scope"
        _op["json"] = scopes

        expected = ["Result", None]

        prepped_request = self._base.prepare_request(_op)
        response = self._base.request(prepped_request, expected, _op)

        return response
