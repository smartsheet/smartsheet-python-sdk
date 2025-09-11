import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestWorkspaces:
    a = None
    b = None
    c = None
    share = None

    def test_create_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.create_workspace(
            smart.models.Workspace({
                'name': 'pytest workspace A ' + smart_setup['now']
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.a = action.result
        action = smart.Workspaces.create_workspace(
            smart.models.Workspace({
                'name': 'pytest workspace B ' + smart_setup['now']
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.b = action.result

    def test_create_folder_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        folder = smart.models.Folder({
            'name': 'Bucket A'
        })
        action = smart.Workspaces.create_folder_in_workspace(
            TestWorkspaces.a.id, folder
        )
        assert action.message == 'SUCCESS'

    def test_list_folders(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_folders(TestWorkspaces.a.id)
        assert action.total_count > 0
        folders = action.result
        assert folders[0].name == 'Bucket A'

    def test_list_workspaces(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_workspaces()
        assert action.total_count > 0

    def test_list_workspaces_with_token_pagination(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_workspaces(pagination_type='token', max_items=100)
        
        # Stronger assertions
        assert hasattr(action, 'data') or hasattr(action, 'result')
        data = action.data if hasattr(action, 'data') else action.result
        assert isinstance(data, list)
        if hasattr(action, 'last_key'):
            assert action.last_key is None or isinstance(action.last_key, str)
        
    def test_list_workspaces_with_last_key(self, smart_setup):
        smart = smart_setup['smart']
        first_action = smart.Workspaces.list_workspaces(pagination_type='token', max_items=100)
        if hasattr(first_action, 'last_key') or (hasattr(first_action, 'result') and hasattr(first_action.result, 'last_key')):
            last_key = getattr(first_action, 'last_key', None) or getattr(first_action.result, 'last_key', None)
            if last_key:
                second_action = smart.Workspaces.list_workspaces(pagination_type='token', last_key=last_key, max_items=100)
                # Stronger assertions
                assert hasattr(second_action, 'data') or hasattr(second_action, 'result')
                data = second_action.data if hasattr(second_action, 'data') else second_action.result
                assert isinstance(data, list)
                
    def test_list_workspaces_traditional_pagination_still_works(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.list_workspaces(page_size=10, page=1)
        assert action.total_count >= 0
        
    def test_list_workspaces_deprecated_parameters_warn(self, smart_setup):
        import warnings
        smart = smart_setup['smart']
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            smart.Workspaces.list_workspaces(page_size=10)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "page_size parameter is deprecated" in str(w[0].message)
            
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            smart.Workspaces.list_workspaces(page=1)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "page parameter is deprecated" in str(w[0].message)
            
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            smart.Workspaces.list_workspaces(include_all=True)
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "include_all parameter is deprecated" in str(w[0].message)

    def test_list_workspaces_token_pagination_validation(self, smart_setup):
        import pytest
        smart = smart_setup['smart']
        
        # Test invalid pagination_type
        with pytest.raises(ValueError, match="pagination_type must be 'token' or None"):
            smart.Workspaces.list_workspaces(pagination_type='invalid')
        
        # Test invalid max_items
        with pytest.raises(ValueError, match="max_items must be a positive integer"):
            smart.Workspaces.list_workspaces(pagination_type='token', max_items=0)
            
        with pytest.raises(ValueError, match="max_items must be a positive integer"):
            smart.Workspaces.list_workspaces(pagination_type='token', max_items=-1)

    def test_create_sheet_from_template_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.create_sheet_in_workspace_from_template(
            TestWorkspaces.b.id,
            smart.models.Sheet({
                'name': 'My Blank Sheet From Template',
                'from_id': 7881304550205316  # Blank Sheet public template id
            })
        )
        assert action.message == 'SUCCESS'

    def test_get_workspace(self, smart_setup):
        smart = smart_setup['smart']
        workspace = smart.Workspaces.get_workspace(TestWorkspaces.b.id)
        assert isinstance(workspace, smart.models.workspace.Workspace)

    def test_copy_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.copy_workspace(
            TestWorkspaces.b.id,
            smart.models.ContainerDestination({
                'new_name': 'pytest workspace C ' + smart_setup['now']
            }),
            include='all'
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.c = action.result

    def test_create_sheet_in_workspace(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.models.Sheet({
            'name': 'pytest_workspace_sheet ' + smart_setup['now'],
            'columns': [{
                'title': 'Slackers',
                'primary': True,
                'type': 'TEXT_NUMBER'
            }]
        })
        action = smart.Workspaces.create_sheet_in_workspace(TestWorkspaces.c.id, sheet);
        sheet = action.result

    def test_share_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.share_workspace(
            TestWorkspaces.c.id,
            smart.models.Share({
                'access_level': 'EDITOR_SHARE',
                'email': smart_setup['users']['moe'].email
            })
        )
        assert action.message == 'SUCCESS'
        TestWorkspaces.share = action.result

    def test_list_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        shares = smart.Workspaces.list_shares(
            TestWorkspaces.c.id
        )
        assert shares.total_count > 0

    def test_get_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        ws = smart.Workspaces.get_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id
        )
        assert isinstance(ws, smart.models.share.Share)

    def test_update_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.update_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id,
            smart.models.Share({
                'access_level': 'ADMIN'
            })
        )
        assert action.message == 'SUCCESS'

    def test_delete_workspace_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.delete_share(
            TestWorkspaces.c.id,
            TestWorkspaces.share.id
        )
        assert action.message == 'SUCCESS'

    def test_get_workspace_metadata(self, smart_setup):
        smart = smart_setup['smart']
        workspace = smart.Workspaces.get_workspace_metadata(TestWorkspaces.a.id)
        assert isinstance(workspace, smart.models.workspace.Workspace)
        assert workspace.id == TestWorkspaces.a.id
        assert workspace.name is not None

    def test_get_workspace_metadata_with_include(self, smart_setup):
        smart = smart_setup['smart']
        workspace = smart.Workspaces.get_workspace_metadata(
            TestWorkspaces.a.id,
            include=['source']
        )
        assert isinstance(workspace, smart.models.workspace.Workspace)
        assert workspace.id == TestWorkspaces.a.id

    def test_get_workspace_children(self, smart_setup):
        smart = smart_setup['smart']
        children = smart.Workspaces.get_workspace_children(TestWorkspaces.a.id)
        assert isinstance(children, smart.models.paginated_children_result.PaginatedChildrenResult)

    def test_get_workspace_children_with_filters(self, smart_setup):
        smart = smart_setup['smart']
        # Test with resource type filter
        children = smart.Workspaces.get_workspace_children(
            TestWorkspaces.a.id,
            children_resource_types=['folders']
        )
        assert isinstance(children, smart.models.paginated_children_result.PaginatedChildrenResult)
        # Verify all children are of the filtered type
        for child in children.data:
            assert isinstance(child, smart.models.folder.Folder)

        # Test with include parameter
        children = smart.Workspaces.get_workspace_children(
            TestWorkspaces.a.id,
            include=['source', 'ownerInfo']
        )
        assert isinstance(children, smart.models.paginated_children_result.PaginatedChildrenResult)

    def test_get_workspace_children_with_pagination(self, smart_setup):
        smart = smart_setup['smart']
        # Test with pagination parameters
        children = smart.Workspaces.get_workspace_children(
            TestWorkspaces.a.id,
            max_items=100
        )
        assert isinstance(children, smart.models.paginated_children_result.PaginatedChildrenResult)

    def test_update_workspace(self, smart_setup):
        smart = smart_setup['smart']
        new_workspace = smart.models.Workspace()
        new_workspace.name = 'Nincompoops'
        action = smart.Workspaces.update_workspace(
            TestWorkspaces.c.id,
            new_workspace
        )
        assert action.message == 'SUCCESS'

    def test_delete_workspace(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Workspaces.delete_workspace(TestWorkspaces.a.id)
        assert action.message == 'SUCCESS'
        action = smart.Workspaces.delete_workspace(TestWorkspaces.b.id)
        assert action.message == 'SUCCESS'
        action = smart.Workspaces.delete_workspace(TestWorkspaces.c.id)
        assert action.message == 'SUCCESS'
