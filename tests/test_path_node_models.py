# pylint: disable=C0103,W0212
"""Unit tests for get_<resource> and get_<resource>_path on path node models."""

from smartsheet.models.folder_path_node import FolderPathNode
from smartsheet.models.report_path_node import ReportPathNode
from smartsheet.models.sheet_path_node import SheetPathNode
from smartsheet.models.sight_path_node import SightPathNode


# ---------------------------------------------------------------------------
# FolderPathNode
# ---------------------------------------------------------------------------

class TestFolderPathNodeGetFolder:

    def test_returns_self_when_no_child_folders(self):
        node = FolderPathNode({"id": 1, "name": "Leaf"})
        assert node.get_leaf_folder() is node

    def test_returns_deepest_nested_folder(self):
        node = FolderPathNode({
            "id": 1,
            "name": "Root",
            "folders": [
                {
                    "id": 2,
                    "name": "Mid",
                    "folders": [
                        {"id": 3, "name": "Leaf"}
                    ],
                }
            ],
        })
        result = node.get_leaf_folder()
        assert result.id == 3
        assert result.name == "Leaf"

    def test_returns_single_child_folder(self):
        node = FolderPathNode({
            "id": 1,
            "name": "Parent",
            "folders": [{"id": 2, "name": "Child"}],
        })
        result = node.get_leaf_folder()
        assert result.id == 2


class TestFolderPathNodeGetFolderPath:

    def test_single_node_returns_its_name(self):
        node = FolderPathNode({"id": 1, "name": "OnlyFolder"})
        assert node.get_leaf_folder_path() == "/OnlyFolder"

    def test_nested_nodes_joined_with_slash(self):
        node = FolderPathNode({
            "id": 1,
            "name": "Root",
            "folders": [
                {
                    "id": 2,
                    "name": "Mid",
                    "folders": [{"id": 3, "name": "Leaf"}],
                }
            ],
        })
        assert node.get_leaf_folder_path() == "/Root/Mid/Leaf"

    def test_empty_node_returns_empty_string(self):
        # FolderPathNode intentionally returns "Root" (not None) for an empty node because
        # the target is a folder itself, not an asset nested inside one.
        node = FolderPathNode({"id": 1, "name": "Root"})
        assert node.get_leaf_folder_path() == "/Root"


# ---------------------------------------------------------------------------
# SheetPathNode
# ---------------------------------------------------------------------------

class TestSheetPathNodeGetSheet:

    def test_returns_sheet_at_root_level(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "sheets": [{"id": 10, "name": "My Sheet"}],
        })
        result = node.get_leaf_sheet()
        assert result is not None
        assert result.id == 10
        assert result.name == "My Sheet"

    def test_returns_sheet_nested_inside_folders(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "sheets": [{"id": 20, "name": "Nested Sheet"}],
                }
            ],
        })
        result = node.get_leaf_sheet()
        assert result is not None
        assert result.id == 20

    def test_returns_none_when_no_sheets(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [{"id": 2, "name": "EmptyFolder"}],
        })
        assert node.get_leaf_sheet() is None

    def test_returns_none_on_empty_node(self):
        node = SheetPathNode()
        assert node.get_leaf_sheet() is None


class TestSheetPathNodeGetSheetPath:

    def test_path_with_sheet_at_root(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "sheets": [{"id": 10, "name": "My Sheet"}],
        })
        assert node.get_leaf_sheet_path() == "/Workspace/My Sheet"

    def test_path_with_nested_sheet(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "sheets": [{"id": 20, "name": "Deep Sheet"}],
                }
            ],
        })
        assert node.get_leaf_sheet_path() == "/Workspace/Folder/Deep Sheet"

    def test_path_deeply_nested(self):
        node = SheetPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Top",
                    "folders": [
                        {
                            "id": 3,
                            "name": "Mid",
                            "sheets": [{"id": 30, "name": "Sheet"}],
                        }
                    ],
                }
            ],
        })
        assert node.get_leaf_sheet_path() == "/Workspace/Top/Mid/Sheet"

    def test_empty_node_returns_none(self):
        node = SheetPathNode()
        assert node.get_leaf_sheet_path() is None


# ---------------------------------------------------------------------------
# ReportPathNode
# ---------------------------------------------------------------------------

class TestReportPathNodeGetReport:

    def test_returns_report_at_root_level(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "reports": [{"id": 10, "name": "My Report"}],
        })
        result = node.get_leaf_report()
        assert result is not None
        assert result.id == 10
        assert result.name == "My Report"

    def test_returns_report_nested_inside_folders(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "reports": [{"id": 20, "name": "Nested Report"}],
                }
            ],
        })
        result = node.get_leaf_report()
        assert result is not None
        assert result.id == 20

    def test_returns_none_when_no_reports(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [{"id": 2, "name": "EmptyFolder"}],
        })
        assert node.get_leaf_report() is None

    def test_returns_none_on_empty_node(self):
        node = ReportPathNode()
        assert node.get_leaf_report() is None


class TestReportPathNodeGetReportPath:

    def test_path_with_report_at_root(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "reports": [{"id": 10, "name": "My Report"}],
        })
        assert node.get_leaf_report_path() == "/Workspace/My Report"

    def test_path_with_nested_report(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "reports": [{"id": 20, "name": "Deep Report"}],
                }
            ],
        })
        assert node.get_leaf_report_path() == "/Workspace/Folder/Deep Report"

    def test_path_deeply_nested(self):
        node = ReportPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Top",
                    "folders": [
                        {
                            "id": 3,
                            "name": "Mid",
                            "reports": [{"id": 30, "name": "Report"}],
                        }
                    ],
                }
            ],
        })
        assert node.get_leaf_report_path() == "/Workspace/Top/Mid/Report"

    def test_empty_node_returns_none(self):
        node = ReportPathNode()
        assert node.get_leaf_report_path() is None


# ---------------------------------------------------------------------------
# SightPathNode
# ---------------------------------------------------------------------------

class TestSightPathNodeGetSight:

    def test_returns_sight_at_root_level(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "sights": [{"id": 10, "name": "My Sight"}],
        })
        result = node.get_leaf_sight()
        assert result is not None
        assert result.id == 10
        assert result.name == "My Sight"

    def test_returns_sight_nested_inside_folders(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "sights": [{"id": 20, "name": "Nested Sight"}],
                }
            ],
        })
        result = node.get_leaf_sight()
        assert result is not None
        assert result.id == 20

    def test_returns_none_when_no_sights(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [{"id": 2, "name": "EmptyFolder"}],
        })
        assert node.get_leaf_sight() is None

    def test_returns_none_on_empty_node(self):
        node = SightPathNode()
        assert node.get_leaf_sight() is None


class TestSightPathNodeGetSightPath:

    def test_path_with_sight_at_root(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "sights": [{"id": 10, "name": "My Sight"}],
        })
        assert node.get_leaf_sight_path() == "/Workspace/My Sight"

    def test_path_with_nested_sight(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Folder",
                    "sights": [{"id": 20, "name": "Deep Sight"}],
                }
            ],
        })
        assert node.get_leaf_sight_path() == "/Workspace/Folder/Deep Sight"

    def test_path_deeply_nested(self):
        node = SightPathNode({
            "id": 1,
            "name": "Workspace",
            "folders": [
                {
                    "id": 2,
                    "name": "Top",
                    "folders": [
                        {
                            "id": 3,
                            "name": "Mid",
                            "sights": [{"id": 30, "name": "Sight"}],
                        }
                    ],
                }
            ],
        })
        assert node.get_leaf_sight_path() == "/Workspace/Top/Mid/Sight"

    def test_empty_node_returns_none(self):
        node = SightPathNode()
        assert node.get_leaf_sight_path() is None
