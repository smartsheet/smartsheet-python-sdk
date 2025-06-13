import pytest
import smartsheet
from smartsheet.models import Share

@pytest.mark.usefixtures("smart_setup")
class TestSharing:
    def test_list_asset_shares(self, smart_setup):
        smart = smart_setup['smart']
        sheet_id = smart_setup['sheet_b'].id
        
        # Test listing shares for a sheet
        action = smart.Sharing.list_asset_shares(
            asset_type='sheet',
            asset_id=sheet_id
        )
        assert action.result is not None
        
    def test_share_asset(self, smart_setup):
        smart = smart_setup['smart']
        sheet_id = smart_setup['sheet_b'].id
        
        # Create a share object
        share_spec = smart.models.Share({
            'email': 'test@example.com',
            'access_level': 'VIEWER'
        })
        
        # Share the sheet
        action = smart.Sharing.share_asset(
            asset_type='sheet',
            asset_id=sheet_id,
            shares=[share_spec],
            send_email=False
        )
        
        # Verify the share was created
        assert action.result is not None
        assert len(action.result) > 0
        assert action.result[0].email == 'test@example.com'
        assert action.result[0].access_level == 'VIEWER'
        
        # Store the share ID for later tests
        share_id = action.result[0].id
        
        # Test get_asset_share
        get_action = smart.Sharing.get_asset_share(
            asset_type='sheet',
            asset_id=sheet_id,
            share_id=share_id
        )
        assert get_action.result is not None
        assert get_action.result.id == share_id
        
        # Test update_share
        update_share_spec = smart.models.Share({
            'id': share_id,
            'access_level': 'EDITOR'
        })
        
        update_action = smart.Sharing.update_share(
            asset_type='sheet',
            asset_id=sheet_id,
            share=update_share_spec
        )
        assert update_action.result is not None
        assert update_action.result.access_level == 'EDITOR'
        
        # Test delete_share
        smart.Sharing.delete_share(
            asset_type='sheet',
            asset_id=sheet_id,
            share_id=share_id
        )
        
        # Verify the share was deleted by trying to get it (should raise exception)
        with pytest.raises(smartsheet.exceptions.ApiError):
            smart.Sharing.get_asset_share(
                asset_type='sheet',
                asset_id=sheet_id,
                share_id=share_id
            )