# pylint: disable=C0103,W0232

import pytest
from smartsheet.models import Workspace, PaginatedChildrenResult, Folder, Sheet, Sight, Report
from smartsheet.exceptions import ApiError
from tests.mock_api.mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiWorkspaces(MockApiTestHelper):
    @clean_api_error
    def test_get_workspace_metadata_no_params(self):
        self.client.as_test_scenario('Get Workspace Metadata - No Params')

        response = self.client.Workspaces.get_workspace_metadata(123)

        assert isinstance(response, Workspace)
        assert response.id == 123
        assert response.name == "Sample Workspace"
        assert response.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert response.access_level == "VIEWER"
        assert response.created_at is not None
        assert response.modified_at is not None
        # Verify source is not included when not requested
        assert not hasattr(response, 'source') or response.source is None

    @clean_api_error
    def test_get_workspace_metadata_include_source(self):
        self.client.as_test_scenario('Get Workspace Metadata - Include Source')

        response = self.client.Workspaces.get_workspace_metadata(
            123,
            include=['source']
        )

        assert isinstance(response, Workspace)
        assert response.id == 123
        assert response.name == "Sample Workspace"
        assert response.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert response.access_level == "ADMIN"
        # Verify source is included with exact values
        assert response.source is not None
        assert response.source.id == 999
        assert response.source.type == "workspace"

    @clean_api_error
    def test_get_workspace_children_no_params(self):
        self.client.as_test_scenario('Get Workspace Children - No Params')

        response = self.client.Workspaces.get_workspace_children(123)

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 4

        # Verify first child (folder) - exact values from scenario
        folder = response.data[0]
        assert isinstance(folder, Folder)
        assert folder.id == 456
        assert folder.name == "Project Folder"
        assert folder.permalink == "https://app.smartsheet.com/b/home?lx=*****************"

        # Verify second child (sheet) - exact values from scenario
        sheet = response.data[1]
        assert isinstance(sheet, Sheet)
        assert sheet.id == 789
        assert sheet.name == "Budget Sheet"
        assert sheet.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert sheet.access_level == "EDITOR"

        # Verify third child (sight) - exact values from scenario
        sight = response.data[2]
        assert isinstance(sight, Sight)
        assert sight.id == 321
        assert sight.name == "Dashboard Overview"
        assert sight.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert sight.access_level == "VIEWER"

        # Verify fourth child (report) - exact values from scenario
        report = response.data[3]
        assert isinstance(report, Report)
        assert report.id == 654
        assert report.name == "Monthly Report"
        assert report.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert report.access_level == "ADMIN"


    @clean_api_error
    def test_get_workspace_children_filter_sheets_and_folders(self):
        self.client.as_test_scenario('Get Workspace Children - Filter Sheets and Folders')

        response = self.client.Workspaces.get_workspace_children(
            123,
            children_resource_types=['folders', 'sheets']
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 3

        # Verify first child (folder)
        folder = response.data[0]
        assert isinstance(folder, Folder)
        assert folder.id == 456
        assert folder.name == "Project Folder"

        # Verify second child (sheet)
        sheet1 = response.data[1]
        assert isinstance(sheet1, Sheet)
        assert sheet1.id == 789
        assert sheet1.name == "Budget Sheet"
        assert sheet1.access_level == "EDITOR"

        # Verify third child (sheet)
        sheet2 = response.data[2]
        assert isinstance(sheet2, Sheet)
        assert sheet2.id == 1234
        assert sheet2.name == "Project Timeline"
        assert sheet2.access_level == "EDITOR"

    @clean_api_error
    def test_get_workspace_children_include_source_and_owner_info(self):
        self.client.as_test_scenario('Get Workspace Children - Include Source and OwnerInfo')

        response = self.client.Workspaces.get_workspace_children(
            123,
            include=['source', 'ownerInfo']
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 4

        # Verify first child (folder) has source but no ownerInfo - real values
        folder = response.data[0]
        assert isinstance(folder, Folder)
        assert folder.id == 456
        assert folder.name == "Project Folder"
        assert folder.source is not None
        assert folder.source.id == 888
        assert folder.source.type == "folder"

        # Verify second child (sheet) has both source and ownerInfo - real values
        sheet = response.data[1]
        assert isinstance(sheet, Sheet)
        assert sheet.id == 789
        assert sheet.name == "Budget Sheet"
        assert sheet.access_level == "EDITOR"
        assert sheet.source is not None
        assert sheet.source.id == 777
        assert sheet.source.type == "sheet"
        assert sheet.owner_id == 1001
        assert sheet.owner == "john.doe@example.com"

        # Verify third child (sight) has source - real values
        sight = response.data[2]
        assert isinstance(sight, Sight)
        assert sight.id == 321
        assert sight.name == "Dashboard Overview"
        assert sight.access_level == "VIEWER"
        assert sight.source is not None
        assert sight.source.id == 666
        assert sight.source.type == "sight"

        # Verify fourth child (report) has source - real values
        report = response.data[3]
        assert isinstance(report, Report)
        assert report.id == 654
        assert report.name == "Monthly Report"
        assert report.access_level == "ADMIN"
        assert report.source is not None
        assert report.source.id == 555
        assert report.source.type == "report"

    @clean_api_error
    def test_get_workspace_children_max_items_and_last_key(self):
        self.client.as_test_scenario('Get Workspace Children - MaxItems and LastKey')

        response = self.client.Workspaces.get_workspace_children(
            123,
            max_items=1000,
            last_key="aslkjf4wlkta4n4900sjfklf499sjwlk4356lkj"
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 1

        # Verify the single child (sheet) matches the expected values
        sheet = response.data[0]
        assert isinstance(sheet, Sheet)
        assert sheet.id == 789
        assert sheet.name == "Budget Sheet"
        assert sheet.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert sheet.access_level == "EDITOR"

        # Verify the lastKey is returned in the response
        assert response.last_key == "xvmnw4mnx8v9wriot20574xvnjoqt4iuhnow490"

    @clean_api_error
    def test_list_workspaces_with_token_pagination_first_page(self):
        self.client.as_test_scenario('List Workspaces - First Page with Pagination')

        response = self.client.Workspaces.list_workspaces(max_items=100)

        assert len(response.data) == 2
        assert isinstance(response.data[0], Workspace)
        assert isinstance(response.data[1], Workspace)
        assert response.data[0].id == 1001
        assert response.data[0].name == "Marketing Workspace"
        assert response.data[1].id == 1002
        assert response.data[1].name == "Sales Workspace"
        assert response.last_key == "eyJsYXN0SWQiOjEwMDJ9"

    @clean_api_error
    def test_list_workspaces_with_last_key_middle_page(self):
        self.client.as_test_scenario('List Workspaces - Middle Page with Pagination')

        response = self.client.Workspaces.list_workspaces(
            last_key='eyJsYXN0SWQiOjEwMDJ9',
            max_items=100
        )

        assert len(response.data) == 2
        assert isinstance(response.data[0], Workspace)
        assert isinstance(response.data[1], Workspace)
        assert response.data[0].id == 1003
        assert response.data[0].name == "Engineering Workspace"
        assert response.data[1].id == 1004
        assert response.data[1].name == "HR Workspace"
        assert response.last_key == "eyJsYXN0SWQiOjEwMDR9"

    @clean_api_error
    def test_list_workspaces_with_last_key_last_page(self):
        self.client.as_test_scenario('List Workspaces - Final Page with Pagination')

        response = self.client.Workspaces.list_workspaces(
            last_key='eyJsYXN0SWQiOjEwMDR9',
            max_items=100
        )

        assert len(response.data) == 1
        assert isinstance(response.data[0], Workspace)
        assert response.data[0].id == 1005
        assert response.data[0].name == "Compliance Workspace"
        assert response.last_key is None
