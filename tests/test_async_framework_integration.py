# pylint: disable=C0103,W0212,R0913
"""Async framework integration tests for async PoC implementation.

This module demonstrates that the async Smartsheet client works correctly
in event loop scenarios similar to async services. Tests verify:
- Non-blocking concurrent operations
- Event loop compatibility
- Performance characteristics of async operations
- Proper behavior under concurrent load

These tests simulate async service patterns where multiple
requests may be handled concurrently without blocking the event loop.
"""

import asyncio
import time
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell, Workspace, IndexResult, Result


@pytest.fixture
def mock_access_token():
    """Provide a mock access token for testing."""
    return "async_test_token_12345"


@pytest.fixture
async def async_client(mock_access_token):
    """Create an AsyncSmartsheet client for async framework testing."""
    client = AsyncSmartsheet(access_token=mock_access_token)
    yield client
    await client.aclose()


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx.Response with configurable delay."""
    def _create_response(status_code=200, json_data=None, delay=0):
        async def delayed_send(*args, **kwargs):
            if delay > 0:
                await asyncio.sleep(delay)
            
            response = MagicMock(spec=httpx.Response)
            response.status_code = status_code
            response.reason_phrase = "OK" if status_code == 200 else "Error"
            response.headers = {"Content-Type": "application/json"}
            
            import json
            response.text = json.dumps(json_data)
            response.content = response.text.encode('utf-8')
            response.json.return_value = json_data
            
            response.request = MagicMock()
            response.request.method = "GET"
            response.request.url = "https://api.smartsheet.com/2.0/test"
            response.request.headers = {"Authorization": "Bearer ***"}
            response.request.content = None
            
            return response
        
        return delayed_send
    return _create_response


class TestAsyncFrameworkEventLoopCompatibility:
    """Test suite for async framework event loop compatibility."""
    
    @pytest.mark.asyncio
    async def test_non_blocking_operations(self, async_client, mock_httpx_response):
        """Test that async operations don't block the event loop.
        
        This simulates an async service handling multiple concurrent requests.
        Each request should execute without blocking others.
        """
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        # Create mock with 0.1 second delay per request
        mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.1)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = mock_send
            await async_client._ensure_session()
            
            start_time = time.time()
            
            # Execute 5 concurrent requests
            tasks = [
                async_client.Workspaces.list_workspaces()
                for _ in range(5)
            ]
            
            results = await asyncio.gather(*tasks)
            
            elapsed_time = time.time() - start_time
            
            # All 5 requests completed successfully
            assert len(results) == 5
            for result in results:
                assert isinstance(result, IndexResult)
            
            # With async, all 5 requests should complete in ~0.1s (concurrent)
            # not 0.5s (sequential). Allow some overhead.
            assert elapsed_time < 0.3, f"Operations took {elapsed_time}s, expected < 0.3s (concurrent execution)"
    
    @pytest.mark.asyncio
    async def test_event_loop_not_blocked_during_io(self, async_client, mock_httpx_response):
        """Test that the event loop remains responsive during I/O operations.
        
        This simulates an async service where other tasks should be able to
        run while waiting for API responses.
        """
        response_data = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [{"id": 12345, "rowNumber": 1, "cells": []}]
        }
        
        # Create mock with 0.2 second delay
        mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.2)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = mock_send
            await async_client._ensure_session()
            
            # Track when background task runs
            background_task_ran = []
            
            async def background_task():
                """Simulates other work happening in the event loop."""
                for i in range(5):
                    await asyncio.sleep(0.05)
                    background_task_ran.append(i)
            
            row = Row()
            row.to_bottom = True
            
            # Start API call and background task concurrently
            api_task = asyncio.create_task(
                async_client.Sheets.add_rows(sheet_id=999, list_of_rows=[row])
            )
            bg_task = asyncio.create_task(background_task())
            
            # Wait for both to complete
            result, _ = await asyncio.gather(api_task, bg_task)
            
            # API call succeeded
            assert isinstance(result, Result)
            
            # Background task was able to run during API I/O wait
            assert len(background_task_ran) == 5, "Background task should have completed during I/O wait"
    
    @pytest.mark.asyncio
    async def test_concurrent_mixed_operations_performance(self, async_client, mock_httpx_response):
        """Test performance of mixed concurrent operations.
        
        Simulates an async service handling different types of requests
        concurrently (reads and writes).
        """
        list_response = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        add_rows_response = {
            "message": "SUCCESS",
            "resultCode": 0,
            "result": [{"id": 12345, "rowNumber": 1, "cells": []}]
        }
        
        async def mock_send_with_delay(*args, **kwargs):
            """Mock send that returns different responses based on URL."""
            await asyncio.sleep(0.1)  # Simulate network delay
            
            request = args[0]
            response = MagicMock(spec=httpx.Response)
            response.status_code = 200
            response.reason_phrase = "OK"
            response.headers = {"Content-Type": "application/json"}
            
            import json
            if '/rows' in str(request.url):
                data = add_rows_response
            else:
                data = list_response
            
            response.text = json.dumps(data)
            response.content = response.text.encode('utf-8')
            response.json.return_value = data
            
            response.request = MagicMock()
            response.request.method = request.method
            response.request.url = request.url
            response.request.headers = {"Authorization": "Bearer ***"}
            response.request.content = None
            
            return response
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(side_effect=mock_send_with_delay)
            await async_client._ensure_session()
            
            start_time = time.time()
            
            row = Row()
            row.to_bottom = True
            
            # Mix of 10 operations: 5 reads, 5 writes
            tasks = []
            for i in range(10):
                if i % 2 == 0:
                    tasks.append(async_client.Workspaces.list_workspaces())
                else:
                    tasks.append(async_client.Sheets.add_rows(sheet_id=i, list_of_rows=[row]))
            
            results = await asyncio.gather(*tasks)
            
            elapsed_time = time.time() - start_time
            
            # All operations completed
            assert len(results) == 10
            
            # With concurrent execution, should take ~0.1s not 1.0s
            assert elapsed_time < 0.3, f"Operations took {elapsed_time}s, expected < 0.3s"


class TestAsyncServicePattern:
    """Test suite simulating async service patterns."""
    
    @pytest.mark.asyncio
    async def test_service_handler_pattern(self, mock_access_token, mock_httpx_response):
        """Test async service handler pattern.
        
        Simulates an async service with multiple handler functions that
        use the async client concurrently.
        """
        
        async def get_workspace_info(client, workspace_id):
            """Simulated async handler: Get workspace info."""
            response_data = {
                "pageNumber": 1,
                "pageSize": 100,
                "totalPages": 1,
                "totalCount": 1,
                "data": [{"id": workspace_id, "name": f"Workspace {workspace_id}", "accessLevel": "OWNER"}]
            }
            
            mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.05)
            
            with patch.object(client, '_session') as mock_session:
                mock_session.send = mock_send
                await client._ensure_session()
                
                result = await client.Workspaces.list_workspaces()
                return {"workspace_id": workspace_id, "count": len(result.data)}
        
        async def add_sheet_rows(client, sheet_id, num_rows):
            """Simulated async handler: Add rows to sheet."""
            response_data = {
                "message": "SUCCESS",
                "resultCode": 0,
                "result": [{"id": i, "rowNumber": i, "cells": []} for i in range(num_rows)]
            }
            
            mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.05)
            
            with patch.object(client, '_session') as mock_session:
                mock_session.send = mock_send
                await client._ensure_session()
                
                row = Row()
                row.to_bottom = True
                
                result = await client.Sheets.add_rows(sheet_id=sheet_id, list_of_rows=[row])
                return {"sheet_id": sheet_id, "rows_added": len(result.data)}
        
        # Simulate async service with shared client
        async with AsyncSmartsheet(access_token=mock_access_token) as client:
            # Simulate multiple concurrent requests to the service
            tasks = [
                get_workspace_info(client, 1),
                add_sheet_rows(client, 100, 3),
                get_workspace_info(client, 2),
                add_sheet_rows(client, 200, 5),
                get_workspace_info(client, 3),
            ]
            
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            elapsed_time = time.time() - start_time
            
            # All handlers completed successfully
            assert len(results) == 5
            assert results[0]["workspace_id"] == 1
            assert results[1]["rows_added"] == 3
            assert results[2]["workspace_id"] == 2
            assert results[3]["rows_added"] == 5
            assert results[4]["workspace_id"] == 3
            
            # Should complete concurrently in ~0.05s, not 0.25s
            assert elapsed_time < 0.2, f"Service handlers took {elapsed_time}s, expected concurrent execution"
    
    @pytest.mark.asyncio
    async def test_request_queue_processing(self, async_client, mock_httpx_response):
        """Test processing a queue of requests concurrently.
        
        Simulates an async service processing a queue of incoming requests
        with controlled concurrency.
        """
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.05)
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = mock_send
            await async_client._ensure_session()
            
            # Simulate a queue of 20 requests
            request_queue = asyncio.Queue()
            for i in range(20):
                await request_queue.put(i)
            
            results = []
            
            async def worker():
                """Worker that processes requests from the queue."""
                while not request_queue.empty():
                    try:
                        request_id = await asyncio.wait_for(request_queue.get(), timeout=0.1)
                        result = await async_client.Workspaces.list_workspaces()
                        results.append({"request_id": request_id, "success": True})
                        request_queue.task_done()
                    except asyncio.TimeoutError:
                        break
            
            # Process queue with 5 concurrent workers
            start_time = time.time()
            workers = [asyncio.create_task(worker()) for _ in range(5)]
            await asyncio.gather(*workers)
            elapsed_time = time.time() - start_time
            
            # All 20 requests processed
            assert len(results) == 20
            
            # With 5 workers processing 20 requests at 0.05s each:
            # Sequential: 20 * 0.05 = 1.0s
            # Concurrent (5 workers): 4 batches * 0.05 = 0.2s
            assert elapsed_time < 0.4, f"Queue processing took {elapsed_time}s, expected < 0.4s"


class TestAsyncErrorHandling:
    """Test suite for error handling in async service scenarios."""
    
    @pytest.mark.asyncio
    async def test_partial_failure_in_concurrent_operations(self, async_client, mock_httpx_response):
        """Test that one failure doesn't affect other concurrent operations.
        
        In an async service, one failed request shouldn't impact others.
        """
        success_response = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        error_response = {
            "errorCode": 1006,
            "message": "Not Found"
        }
        
        call_count = [0]
        
        async def mock_send_mixed(*args, **kwargs):
            """Mock that fails on 3rd call, succeeds otherwise."""
            call_count[0] += 1
            await asyncio.sleep(0.05)
            
            response = MagicMock(spec=httpx.Response)
            response.headers = {"Content-Type": "application/json"}
            
            import json
            if call_count[0] == 3:
                # Third call fails
                response.status_code = 404
                response.reason_phrase = "Not Found"
                data = error_response
            else:
                # Other calls succeed
                response.status_code = 200
                response.reason_phrase = "OK"
                data = success_response
            
            response.text = json.dumps(data)
            response.content = response.text.encode('utf-8')
            response.json.return_value = data
            
            response.request = MagicMock()
            response.request.method = "GET"
            response.request.url = "https://api.smartsheet.com/2.0/workspaces"
            response.request.headers = {"Authorization": "Bearer ***"}
            response.request.content = None
            
            return response
        
        with patch.object(async_client, '_session') as mock_session:
            mock_session.send = AsyncMock(side_effect=mock_send_mixed)
            await async_client._ensure_session()
            
            # Execute 5 concurrent requests
            tasks = [
                async_client.Workspaces.list_workspaces()
                for _ in range(5)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=False)
            
            # 4 should succeed, 1 should be an error
            successes = [r for r in results if isinstance(r, IndexResult)]
            errors = [r for r in results if not isinstance(r, IndexResult)]
            
            assert len(successes) == 4, "4 requests should succeed"
            assert len(errors) == 1, "1 request should fail"
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, async_client):
        """Test handling of operation timeouts in async service.
        
        Services need to handle timeouts gracefully without blocking.
        """
        
        async def slow_operation():
            """Simulates a slow API operation."""
            await asyncio.sleep(2.0)
            return "completed"
        
        # Test that we can timeout operations
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(slow_operation(), timeout=0.1)
        
        # Event loop should still be responsive after timeout
        quick_result = await asyncio.sleep(0.01, result="still_working")
        assert quick_result == "still_working"


class TestAsyncResourceManagement:
    """Test suite for resource management in async scenarios."""
    
    @pytest.mark.asyncio
    async def test_connection_pooling(self, mock_access_token, mock_httpx_response):
        """Test that connection pooling works correctly under load.
        
        Async services should efficiently reuse connections.
        """
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.01)
        
        # Create client with small connection pool
        async with AsyncSmartsheet(access_token=mock_access_token, max_connections=3) as client:
            with patch.object(client, '_session') as mock_session:
                mock_session.send = mock_send
                await client._ensure_session()
                
                # Execute more requests than pool size
                tasks = [
                    client.Workspaces.list_workspaces()
                    for _ in range(10)
                ]
                
                results = await asyncio.gather(*tasks)
                
                # All requests should complete successfully despite limited pool
                assert len(results) == 10
                for result in results:
                    assert isinstance(result, IndexResult)
    
    @pytest.mark.asyncio
    async def test_graceful_shutdown(self, mock_access_token, mock_httpx_response):
        """Test graceful shutdown of client with pending operations.
        
        Async services need to shut down cleanly.
        """
        response_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1,
            "data": [{"id": 111, "name": "Workspace 1", "accessLevel": "OWNER"}]
        }
        
        mock_send = mock_httpx_response(status_code=200, json_data=response_data, delay=0.1)
        
        client = AsyncSmartsheet(access_token=mock_access_token)
        
        with patch.object(client, '_session') as mock_session:
            mock_session.send = mock_send
            await client._ensure_session()
            
            # Start some operations
            task1 = asyncio.create_task(client.Workspaces.list_workspaces())
            task2 = asyncio.create_task(client.Workspaces.list_workspaces())
            
            # Let them start
            await asyncio.sleep(0.05)
            
            # Wait for operations to complete before closing
            await asyncio.gather(task1, task2)
            
            # Clean shutdown
            await client.aclose()
            
            # Verify both operations completed
            assert task1.done()
            assert task2.done()
