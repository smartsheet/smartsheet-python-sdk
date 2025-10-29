# pylint: disable=C0103,W0232

import pytest
from smartsheet.models import Folder, PaginatedChildrenResult, Sheet, Sight, Report
from smartsheet.exceptions import ApiError
from tests.mock_api.mock_api_test_helper import MockApiTestHelper, clean_api_error


class TestMockApiFolders(MockApiTestHelper):
    @clean_api_error
    def test_get_folder_metadata_no_params(self):
        self.client.as_test_scenario('Get Folder Metadata - No Params')

        response = self.client.Folders.get_folder_metadata(456)

        assert isinstance(response, Folder)
        assert response.id == 456
        assert response.name == "Project Folder"
        assert response.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        # Verify source is not included when not requested
        assert not hasattr(response, 'source') or response.source is None

    @clean_api_error
    def test_get_folder_metadata_include_source(self):
        self.client.as_test_scenario('Get Folder Metadata - Include Source')

        response = self.client.Folders.get_folder_metadata(
            456,
            include=['source']
        )

        assert isinstance(response, Folder)
        assert response.id == 456
        assert response.name == "Project Folder"
        # Verify source is included
        assert response.source is not None
        assert response.source.id == 888
        assert response.source.type == "folder"

    @clean_api_error
    def test_get_folder_children_no_params(self):
        self.client.as_test_scenario('Get Folder Children - No Params')

        response = self.client.Folders.get_folder_children(456)

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 4

        # Verify first child (subfolder)
        subfolder = response.data[0]
        assert isinstance(subfolder, Folder)
        assert subfolder.id == 987
        assert subfolder.name == "Subfolder"

        # Verify second child (sheet)
        sheet = response.data[1]
        assert isinstance(sheet, Sheet)
        assert sheet.id == 234
        assert sheet.name == "Task List"
        assert sheet.access_level == "EDITOR"

        # Verify third child (sight)
        sight = response.data[2]
        assert isinstance(sight, Sight)
        assert sight.id == 567
        assert sight.name == "Project Dashboard"
        assert sight.access_level == "EDITOR"

        # Verify fourth child (report)
        report = response.data[3]
        assert isinstance(report, Report)
        assert report.id == 890
        assert report.name == "Status Report"
        assert report.access_level == "VIEWER"

    @clean_api_error
    def test_get_folder_children_filter_sights_and_reports(self):
        self.client.as_test_scenario('Get Folder Children - Filter Sights and Reports')

        response = self.client.Folders.get_folder_children(
            456,
            children_resource_types=['reports', 'sights']
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 3

        # Verify first child (sight)
        sight1 = response.data[0]
        assert isinstance(sight1, Sight)
        assert sight1.id == 567
        assert sight1.name == "Project Dashboard"
        assert sight1.access_level == "EDITOR"

        # Verify second child (sight)
        sight2 = response.data[1]
        assert isinstance(sight2, Sight)
        assert sight2.id == 1567
        assert sight2.name == "Executive Summary"
        assert sight2.access_level == "VIEWER"

        # Verify third child (report)
        report = response.data[2]
        assert isinstance(report, Report)
        assert report.id == 890
        assert report.name == "Status Report"
        assert report.access_level == "VIEWER"

    @clean_api_error
    def test_get_folder_children_include_source_and_owner_info(self):
        self.client.as_test_scenario('Get Folder Children - Include Source and OwnerInfo')

        response = self.client.Folders.get_folder_children(
            456,
            include=['source', 'ownerInfo']
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 4

        # Verify first child (subfolder) has source but no ownerInfo
        subfolder = response.data[0]
        assert isinstance(subfolder, Folder)
        assert subfolder.id == 987
        assert subfolder.name == "Subfolder"
        assert subfolder.source is not None
        assert subfolder.source.id == 444
        assert subfolder.source.type == "folder"

        # Verify second child (sheet) has both source and ownerInfo
        sheet = response.data[1]
        assert isinstance(sheet, Sheet)
        assert sheet.id == 234
        assert sheet.name == "Task List"
        assert sheet.access_level == "EDITOR"
        assert sheet.source is not None
        assert sheet.source.id == 333
        assert sheet.source.type == "sheet"
        assert sheet.owner_id == 2002
        assert sheet.owner == "jane.smith@example.com"

        # Verify third child (sight) has source
        sight = response.data[2]
        assert isinstance(sight, Sight)
        assert sight.id == 567
        assert sight.name == "Project Dashboard"
        assert sight.access_level == "EDITOR"
        assert sight.source is not None
        assert sight.source.id == 222
        assert sight.source.type == "sight"

        # Verify fourth child (report) has source
        report = response.data[3]
        assert isinstance(report, Report)
        assert report.id == 890
        assert report.name == "Status Report"
        assert report.access_level == "VIEWER"
        assert report.source is not None
        assert report.source.id == 111
        assert report.source.type == "report"

    @clean_api_error
    def test_get_folder_children_max_items_and_last_key(self):
        self.client.as_test_scenario('Get Folder Children - MaxItems and LastKey')

        response = self.client.Folders.get_folder_children(
            456,
            max_items=100,
            last_key="aslkjf4wlkta4n4900sjfklf499sjwlk4356lkj"
        )

        assert isinstance(response, PaginatedChildrenResult)
        assert len(response.data) == 1

        # Verify the single child (sight) matches the expected values
        sight = response.data[0]
        assert isinstance(sight, Sight)
        assert sight.id == 567
        assert sight.name == "Project Dashboard"
        assert sight.permalink == "https://app.smartsheet.com/b/home?lx=*****************"
        assert sight.access_level == "EDITOR"

        # Verify the lastKey is returned in the response
        assert response.last_key == "xvmnw4mnx8v9wriot20574xvnjoqt4iuhnow490"
