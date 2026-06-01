# pylint: disable=C0103,W0212,R0913
"""Tests for async PoC implementation.

This module contains comprehensive tests for the async Smartsheet client,
including AsyncSmartsheet, AsyncSheets, and AsyncWorkspaces. Tests use
mocked HTTP responses to avoid making real API calls.
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell, Workspace, Error, Result, IndexResult
from smartsheet.exceptions import ApiError


@pytest.fixture
def mock_access_token():
    """Provide a mock access token for testing."""
    return "test_access_token_12345"


@pytest.fixture
async def async_client(mock_access_token):
    """Create an AsyncSmartsheet client for testing.
    
    This fixture creates a client and ensures proper cleanup after tests.
    """
    client = AsyncSmartsheet(access_token=mock_access_token)
    yield client
    await client.aclose()


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx.Response object."""
    def _create_response(status_code=200, json_data=None, headers=None):
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.reason_phrase = "OK" if status_code == 200 else "Error"
        response.headers = headers or {"Content-Type": "application/json"}
        
        if json_data:
            response.text = json.dumps(json_data)
            response.content = response.text.encode('utf-8')
            response.json.return_value = json_data
        else:
            response.text = ""
            response.content = b""
            response.json.side_effect = ValueError("No JSON")
        
        # Mock request object
        response.request = MagicMock()
        response.request.method = "GET"
        response.request.url = "https://api.smartsheet.com/2.0/test"
        response.request.headers = {"Authorization": "Bearer ***"}
        response.request.content = None
        
        return response
    return _create_response


class TestAsyncSmartsheetClient:
    """Test suite for AsyncSmartsheet client initialization and lifecycle."""
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, mock_access_token):
        """Test that AsyncSmartsheet client initializes correctly."""
        client = AsyncSmartsheet(access_token=mock_access_token)
        
        assert client._access_token == mock_access_token
        assert client._session is None  # Session not created until first use
        assert client.raise_exceptions is False
        
        await client.aclose()
    
    @pytest.mark.asyncio
    async def test_client_initialization_from_env(self, monkeypatch):
        """Test client initialization using environment variable."""
        test_token = "env_token_12345"
        monkeypatch.setenv("SMARTSHEET_ACCESS_TOKEN", test_token)
        
        client = AsyncSmartsheet()
        assert client._access_token == test_token
        
        await client.aclose()
    
    @pytest.mark.asyncio
    async def test_client_initialization_no_token(self):
        """Test that client raises ValueError when no token is provided."""
        with pytest.raises(ValueError, match="Access Token must be set"):
            AsyncSmartsheet()
    
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_access_token):
        """Test AsyncSmartsheet as an async context manager."""
        async with AsyncSmartsheet(access_token=mock_access_token) as client:
            assert client._access_token == mock_access_token
            # Session should be created on context entry
            await client._ensure_session()
            assert client._session is not None
        
        # Session should be closed after context exit
        # Note: We can't directly check if session is closed, but we verify no errors
    
    @pytest.mark.asyncio
    async def test_manual_close(self, mock_access_token):
        """Test manual resource cleanup with aclose()."""
        client = AsyncSmartsheet(access_token=mock_access_token)
        await client._ensure_session()
        
        assert client._session is not None
        
        await client.aclose()
        assert client._session is None
    
    @pytest.mark.asyncio
    async def test_errors_as_exceptions(self, async_client):
        """Test errors_as_exceptions configuration."""
        assert async_client.raise_exceptions is False
        
        async_client.errors_as_exceptions(True)
        assert async_client.raise_exceptions is True
        
        async_client.errors_as_exceptions(False)
        assert async_client.raise_exceptions is False
    
    @pytest.mark.asyncio
    async def test_assume_user(self, async_client):
        """Test assume_user functionality."""
        assert async_client._assume_user is None
        
        async_client.assume_user("test@example.com")
        assert async_client._assume_user == "test%40example.com"
        
        async_client.assume_user(None)
        assert async_client._assume_user is None


class TestAsyncSheetsAddRows:
    """Test suite for AsyncSheets.add_rows() method."""
    
    @pytest.mark.asyncio
    async def test_add_rows_success(self, async_client, mock_httpx_response):
        """Test successful add_rows operation."""
        # Mock response data
        response_data = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [
                {
                    "id": 12345,
                    "rowNumber": 1,
                    "cells": [
                        {"columnId": 111, "value": "Test Value 1"},
                        {"columnId": 222, "value": "Test Value 2"}
                    ]
                }
            ]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        # Mock the HTTP client
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            # Create test row
            row = Row()
            row.to_bottom = True
            row.cells = [
                Cell({'column_id': 111, 'value': 'Test Value 1'}),
                Cell({'column_id': 222, 'value': 'Test Value 2'})
            ]
            
            # Execute add_rows
            result = await async_client.Sheets.add_rows(sheet_id=999, list_of_rows=[row])
            
            # Verify result
            assert isinstance(result, Result)
            assert result.message == "SUCCESS"
            assert len(result.data) == 1
            assert result.data[0].id == 12345
    
    @pytest.mark.asyncio
    async def test_add_rows_single_row(self, async_client, mock_httpx_response):
        """Test add_rows with a single Row object (not in a list)."""
        response_data = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [{"id": 12345, "rowNumber": 1, "cells": []}]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            # Pass single Row object instead of list
            row = Row()
            row.to_bottom = True
            
            result = await async_client.Sheets.add_rows(sheet_id=999, list_of_rows=row)
            
            assert isinstance(result, Result)
            assert len(result.data) == 1
    
    @pytest.mark.asyncio
    async def test_add_rows_error_response(self, async_client, mock_httpx_response):
        """Test add_rows with error response."""
        error_data = {
            "errorCode": 1006,
            "message": "Not Found",
            "refId": "test-ref-id"
        }
        
        mock_response = mock_httpx_response(status_code=404, json_data=error_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            row = Row()
            row.to_bottom = True
            
            result = await async_client.Sheets.add_rows(sheet_id=999, list_of_rows=[row])
            
            # With raise_exceptions=False (default), should return Error object
            assert isinstance(result, Error)
            assert result.result.status_code == 404
            assert result.result.code == 1006
    
    @pytest.mark.asyncio
    async def test_add_rows_with_exceptions_enabled(self, async_client, mock_httpx_response):
        """Test add_rows raises exception when errors_as_exceptions is enabled."""
        async_client.errors_as_exceptions(True)
        
        error_data = {
            "errorCode": 1006,
            "message": "Not Found",
            "refId": "test-ref-id"
        }
        
        mock_response = mock_httpx_response(status_code=404, json_data=error_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            row = Row()
            row.to_bottom = True
            
            with pytest.raises(ApiError):
                await async_client.Sheets.add_rows(sheet_id=999, list_of_rows=[row])


class TestAsyncWorkspacesListWorkspaces:
    """Test suite for AsyncWorkspaces.list_workspaces() method."""
    
    @pytest.mark.asyncio
    async def test_list_workspaces_success(self, async_client, mock_httpx_response):
        """Test successful list_workspaces operation."""
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 2,
            "data": [
                {"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"},
                {"id": 222, "name": "Workspace 2", "accessLevel": "ADMIN"}
            ]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            result = await async_client.Workspaces.list_workspaces()
            
            assert isinstance(result, IndexResult)
            assert len(result.data) == 2
            assert result.data[0].name == "Workspace 1"
            assert result.data[1].name == "Workspace 2"
            assert result.total_count == 2
    
    @pytest.mark.asyncio
    async def test_list_workspaces_token_pagination(self, async_client, mock_httpx_response):
        """Test list_workspaces with token-based pagination."""
        response_data = {
            "data": [
                {"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}
            ],
            "nextToken": "next_page_token_abc123"
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            result = await async_client.Workspaces.list_workspaces(
                pagination_type='token',
                max_items=100
            )
            
            assert isinstance(result, IndexResult)
            assert len(result.data) == 1
            assert hasattr(result, 'next_token')
            assert result.next_token == "next_page_token_abc123"
    
    @pytest.mark.asyncio
    async def test_list_workspaces_legacy_pagination(self, async_client, mock_httpx_response):
        """Test list_workspaces with legacy pagination parameters."""
        response_data = {
            "pageNumber": 2,
            "pageSize": 50,
            "totalPages": 3,
            "totalCount": 125,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            # Should issue deprecation warning
            with pytest.warns(DeprecationWarning):
                result = await async_client.Workspaces.list_workspaces(
                    page_size=50,
                    page=2
                )
            
            assert isinstance(result, IndexResult)
            assert result.page_number == 2
            assert result.total_pages == 3
    
    @pytest.mark.asyncio
    async def test_list_workspaces_invalid_pagination_type(self, async_client):
        """Test list_workspaces with invalid pagination_type."""
        with pytest.raises(ValueError, match="pagination_type must be 'token' or None"):
            await async_client.Workspaces.list_workspaces(pagination_type='invalid')
    
    @pytest.mark.asyncio
    async def test_list_workspaces_invalid_max_items(self, async_client):
        """Test list_workspaces with invalid max_items."""
        with pytest.raises(ValueError, match="max_items must be a positive integer"):
            await async_client.Workspaces.list_workspaces(
                pagination_type='token',
                max_items=0
            )


class TestAsyncConcurrentOperations:
    """Test suite for concurrent async operations."""
    
    @pytest.mark.asyncio
    async def test_concurrent_add_rows(self, async_client, mock_httpx_response):
        """Test multiple concurrent add_rows operations."""
        response_data = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [{"id": 12345, "rowNumber": 1, "cells": []}]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            # Create multiple rows for different sheets
            row = Row()
            row.to_bottom = True
            
            # Execute multiple add_rows concurrently
            tasks = [
                async_client.Sheets.add_rows(sheet_id=i, list_of_rows=[row])
                for i in range(1, 6)
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Verify all operations completed successfully
            assert len(results) == 5
            for result in results:
                assert isinstance(result, Result)
                assert result.message == "SUCCESS"
    
    @pytest.mark.asyncio
    async def test_concurrent_list_workspaces(self, async_client, mock_httpx_response):
        """Test multiple concurrent list_workspaces operations."""
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        mock_response = mock_httpx_response(status_code=200, json_data=response_data)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=mock_response)
            await async_client._ensure_session()
            
            # Execute multiple list_workspaces concurrently
            tasks = [
                async_client.Workspaces.list_workspaces()
                for _ in range(5)
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Verify all operations completed successfully
            assert len(results) == 5
            for result in results:
                assert isinstance(result, IndexResult)
                assert len(result.data) == 1
    
    @pytest.mark.asyncio
    async def test_mixed_concurrent_operations(self, async_client, mock_httpx_response):
        """Test mixed concurrent operations (add_rows and list_workspaces)."""
        add_rows_response = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [{"id": 12345, "rowNumber": 1, "cells": []}]
        }
        
        list_workspaces_response = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        # Create different responses based on URL
        def create_response(*args, **kwargs):
            request = args[0]
            if '/rows' in str(request.url):
                return mock_httpx_response(status_code=200, json_data=add_rows_response)
            else:
                return mock_httpx_response(status_code=200, json_data=list_workspaces_response)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(side_effect=create_response)
            await async_client._ensure_session()
            
            row = Row()
            row.to_bottom = True
            
            # Mix of different operations
            tasks = [
                async_client.Sheets.add_rows(sheet_id=1, list_of_rows=[row]),
                async_client.Workspaces.list_workspaces(),
                async_client.Sheets.add_rows(sheet_id=2, list_of_rows=[row]),
                async_client.Workspaces.list_workspaces(),
            ]
            
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 4
            assert isinstance(results[0], Result)
            assert isinstance(results[1], IndexResult)
            assert isinstance(results[2], Result)
            assert isinstance(results[3], IndexResult)


class TestAsyncRetryLogic:
    """Test suite for async retry logic and error handling."""
    
    @pytest.mark.asyncio
    async def test_retry_on_rate_limit(self, async_client, mock_httpx_response):
        """Test retry logic on rate limit error (4003)."""
        rate_limit_response = mock_httpx_response(
            status_code=429,
            json_data={"errorCode": 4003, "message": "Rate limit exceeded"}
        )
        
        success_response = mock_httpx_response(
            status_code=200,
            json_data={
                "pageNumber": 1,
                "pageSize": 100,
                "totalPages": 1,
                "totalCount": 1,
                "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
            }
        )
        
        with patch.object(async_client, '_session') as mock_session:
            # First call returns rate limit, second call succeeds
            mock_session.send = AsyncMock(side_effect=[rate_limit_response, success_response])
            await async_client._ensure_session()
            
            # Mock asyncio.sleep to avoid actual delays in tests
            with patch('asyncio.sleep', new_callable=AsyncMock):
                result = await async_client.Workspaces.list_workspaces()
            
            # Should succeed after retry
            assert isinstance(result, IndexResult)
            assert len(result.data) == 1
            
            # Verify send was called twice (initial + 1 retry)
            assert mock_session.send.call_count == 2
    
    @pytest.mark.asyncio
    async def test_no_retry_on_client_error(self, async_client, mock_httpx_response):
        """Test that client errors (4xx) don't trigger retry."""
        error_response = mock_httpx_response(
            status_code=400,
            json_data={"errorCode": 1002, "message": "Invalid request"}
        )
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(return_value=error_response)
            await async_client._ensure_session()
            
            row = Row()
            row.to_bottom = True
            
            result = await async_client.Sheets.add_rows(sheet_id=999, list_of_rows=[row])
            
            # Should return error without retry
            assert isinstance(result, Error)
            
            # Verify send was called only once (no retry)
            assert mock_session.send.call_count == 1
    
    @pytest.mark.asyncio
    async def test_max_retry_time_exceeded(self, async_client, mock_httpx_response):
        """Test that retries stop after max_retry_time is exceeded."""
        rate_limit_response = mock_httpx_response(
            status_code=429,
            json_data={"errorCode": 4003, "message": "Rate limit exceeded"}
        )
        
        with patch.object(async_client, '_session') as mock_session:
            # Always return rate limit error
            mock_session.send = AsyncMock(return_value=rate_limit_response)
            await async_client._ensure_session()
            
            # Mock asyncio.sleep to avoid actual delays
            with patch('asyncio.sleep', new_callable=AsyncMock):
                result = await async_client.Workspaces.list_workspaces()
            
            # Should eventually give up and return error
            assert isinstance(result, Error)
            assert result.result.code == 4003


class TestAsyncResourceCleanup:
    """Test suite for proper resource cleanup."""
    
    @pytest.mark.asyncio
    async def test_context_manager_cleanup_on_exception(self, mock_access_token, mock_httpx_response):
        """Test that resources are cleaned up even when exception occurs."""
        error_response = mock_httpx_response(
            status_code=500,
            json_data={"errorCode": 4004, "message": "Server error"}
        )
        
        try:
            async with AsyncSmartsheet(access_token=mock_access_token) as client:
                client.errors_as_exceptions(True)
                
                with patch.object(client, '_session') as mock_session:
                    mock_session.send = AsyncMock(return_value=error_response)
                    await client._ensure_session()
                    
                    # This should raise an exception
                    await client.Workspaces.list_workspaces()
        except ApiError:
            pass  # Expected
        
        # Client should be closed even after exception
        # (We can't directly verify, but no exception should occur)
    
    @pytest.mark.asyncio
    async def test_multiple_close_calls(self, mock_access_token):
        """Test that calling aclose() multiple times is safe."""
        client = AsyncSmartsheet(access_token=mock_access_token)
        await client._ensure_session()
        
        # Close multiple times - should not raise exception
        await client.aclose()
        await client.aclose()
        await client.aclose()
        
        assert client._session is None
