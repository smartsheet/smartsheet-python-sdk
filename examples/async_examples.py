#!/usr/bin/env python3
"""
Smartsheet Python SDK - Async Examples

This module demonstrates how to use the async features of the Smartsheet Python SDK.
These examples show the PoC implementation including add_rows and list_workspaces.

Requirements:
    - smartsheet-python-sdk
    - httpx

Installation:
    pip install smartsheet-python-sdk httpx

Setup:
    Set your Smartsheet access token as an environment variable:
    export SMARTSHEET_ACCESS_TOKEN="your_token_here"
    
    Or pass it directly to the AsyncSmartsheet constructor.

Usage:
    python async_examples.py
"""

import asyncio
import os
from typing import List

from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell, Error, Result, IndexResult


# =============================================================================
# Example 1: Basic Async Client Usage
# =============================================================================

async def example_basic_usage():
    """
    Demonstrates basic async client usage with context manager.
    
    This is the recommended way to use the async client as it automatically
    handles resource cleanup.
    """
    print("\n" + "="*70)
    print("Example 1: Basic Async Client Usage")
    print("="*70)
    
    # Get access token from environment
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    # Use async context manager (recommended)
    async with AsyncSmartsheet(access_token=access_token) as client:
        print("✓ Client initialized with context manager")
        
        # List workspaces
        result = await client.Workspaces.list_workspaces()
        
        if isinstance(result, Error):
            print(f"✗ Error: {result.result.message}")
        else:
            print(f"✓ Found {len(result.data)} workspaces")
            for workspace in result.data[:5]:  # Show first 5
                print(f"  - {workspace.name} (ID: {workspace.id})")
    
    print("✓ Client automatically closed")


# =============================================================================
# Example 2: Manual Resource Management
# =============================================================================

async def example_manual_cleanup():
    """
    Demonstrates manual resource management without context manager.
    
    Use this approach when you need more control over the client lifecycle.
    Always remember to call aclose() when done!
    """
    print("\n" + "="*70)
    print("Example 2: Manual Resource Management")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    # Create client without context manager
    client = AsyncSmartsheet(access_token=access_token)
    print("✓ Client initialized")
    
    try:
        result = await client.Workspaces.list_workspaces()
        
        if isinstance(result, Error):
            print(f"✗ Error: {result.result.message}")
        else:
            print(f"✓ Found {len(result.data)} workspaces")
    finally:
        # IMPORTANT: Always close the client to release resources
        await client.aclose()
        print("✓ Client manually closed")


# =============================================================================
# Example 3: Adding Rows to a Sheet
# =============================================================================

async def example_add_rows(sheet_id: int, column_ids: List[int]):
    """
    Demonstrates adding rows to a sheet asynchronously.
    
    Args:
        sheet_id: The ID of the sheet to add rows to
        column_ids: List of column IDs for the cells (must have at least 3)
    """
    print("\n" + "="*70)
    print("Example 3: Adding Rows to a Sheet")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # Create first row
        row1 = Row()
        row1.to_bottom = True  # Add to bottom of sheet
        row1.cells = [
            Cell({'column_id': column_ids[0], 'value': 'Task 1'}),
            Cell({'column_id': column_ids[1], 'value': 'In Progress'}),
            Cell({'column_id': column_ids[2], 'value': 'High'})
        ]
        
        # Create second row
        row2 = Row()
        row2.to_bottom = True
        row2.cells = [
            Cell({'column_id': column_ids[0], 'value': 'Task 2'}),
            Cell({'column_id': column_ids[1], 'value': 'Not Started'}),
            Cell({'column_id': column_ids[2], 'value': 'Medium'})
        ]
        
        print(f"Adding 2 rows to sheet {sheet_id}...")
        
        # Add rows asynchronously
        result = await client.Sheets.add_rows(sheet_id, [row1, row2])
        
        if isinstance(result, Error):
            print(f"✗ Error: {result.result.message}")
            print(f"  Status Code: {result.result.status_code}")
            print(f"  Error Code: {result.result.code}")
        else:
            print(f"✓ Successfully added {len(result.data)} rows")
            for row in result.data:
                print(f"  - Row ID: {row.id}, Row Number: {row.row_number}")


# =============================================================================
# Example 4: Listing Workspaces with Token Pagination
# =============================================================================

async def example_list_workspaces_pagination():
    """
    Demonstrates listing workspaces with token-based pagination.
    
    Token pagination is more efficient than legacy offset-based pagination
    and is the recommended approach for new code.
    """
    print("\n" + "="*70)
    print("Example 4: Listing Workspaces with Token Pagination")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # First page with token pagination
        print("Fetching first page (max 100 items)...")
        result = await client.Workspaces.list_workspaces(
            pagination_type='token',
            max_items=100
        )
        
        if isinstance(result, Error):
            print(f"✗ Error: {result.result.message}")
            return
        
        print(f"✓ Found {len(result.data)} workspaces on first page")
        for workspace in result.data:
            print(f"  - {workspace.name} (ID: {workspace.id}, Access: {workspace.access_level})")
        
        # Check if there are more pages
        if hasattr(result, 'next_token') and result.next_token:
            print(f"\n✓ More results available (next_token: {result.next_token[:20]}...)")
            print("Fetching next page...")
            
            next_result = await client.Workspaces.list_workspaces(
                pagination_type='token',
                last_key=result.next_token,
                max_items=100
            )
            
            if not isinstance(next_result, Error):
                print(f"✓ Found {len(next_result.data)} workspaces on second page")
        else:
            print("\n✓ No more pages available")


# =============================================================================
# Example 5: Concurrent Operations
# =============================================================================

async def example_concurrent_operations(sheet_ids: List[int], column_ids: List[int]):
    """
    Demonstrates running multiple operations concurrently.
    
    This is one of the main benefits of async - you can make multiple
    API calls at the same time, significantly improving throughput.
    
    Args:
        sheet_ids: List of sheet IDs to add rows to
        column_ids: List of column IDs for the cells
    """
    print("\n" + "="*70)
    print("Example 5: Concurrent Operations")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # Create a row to add to multiple sheets
        row = Row()
        row.to_bottom = True
        row.cells = [
            Cell({'column_id': column_ids[0], 'value': 'Concurrent Task'}),
            Cell({'column_id': column_ids[1], 'value': 'Automated'}),
            Cell({'column_id': column_ids[2], 'value': 'Low'})
        ]
        
        print(f"Adding rows to {len(sheet_ids)} sheets concurrently...")
        
        # Create tasks for concurrent execution
        tasks = [
            client.Sheets.add_rows(sheet_id, [row])
            for sheet_id in sheet_ids
        ]
        
        # Execute all tasks concurrently
        import time
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        elapsed_time = time.time() - start_time
        
        # Process results
        success_count = 0
        error_count = 0
        
        for sheet_id, result in zip(sheet_ids, results):
            if isinstance(result, Error):
                print(f"✗ Sheet {sheet_id}: Error - {result.result.message}")
                error_count += 1
            else:
                print(f"✓ Sheet {sheet_id}: Added {len(result.data)} rows")
                success_count += 1
        
        print(f"\n✓ Completed {len(sheet_ids)} operations in {elapsed_time:.2f} seconds")
        print(f"  Success: {success_count}, Errors: {error_count}")


# =============================================================================
# Example 6: Mixed Concurrent Operations
# =============================================================================

async def example_mixed_concurrent_operations(sheet_id: int, column_ids: List[int]):
    """
    Demonstrates running different types of operations concurrently.
    
    You can mix different API calls (add_rows, list_workspaces, etc.)
    and execute them all at the same time.
    
    Args:
        sheet_id: Sheet ID for add_rows operation
        column_ids: List of column IDs for the cells
    """
    print("\n" + "="*70)
    print("Example 6: Mixed Concurrent Operations")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # Create row for add_rows operation
        row = Row()
        row.to_bottom = True
        row.cells = [
            Cell({'column_id': column_ids[0], 'value': 'Mixed Operation Task'})
        ]
        
        print("Running mixed operations concurrently...")
        
        # Execute different operations concurrently
        results = await asyncio.gather(
            client.Workspaces.list_workspaces(),
            client.Sheets.add_rows(sheet_id, [row]),
            client.Workspaces.list_workspaces(pagination_type='token', max_items=50),
        )
        
        workspaces1, add_result, workspaces2 = results
        
        # Process results
        if not isinstance(workspaces1, Error):
            print(f"✓ Operation 1: Found {len(workspaces1.data)} workspaces (legacy pagination)")
        
        if not isinstance(add_result, Error):
            print(f"✓ Operation 2: Added {len(add_result.data)} rows to sheet {sheet_id}")
        
        if not isinstance(workspaces2, Error):
            print(f"✓ Operation 3: Found {len(workspaces2.data)} workspaces (token pagination)")


# =============================================================================
# Example 7: Error Handling with Error Objects
# =============================================================================

async def example_error_handling_objects():
    """
    Demonstrates error handling using Error objects (default behavior).
    
    By default, the async client returns Error objects instead of raising
    exceptions. This gives you fine-grained control over error handling.
    """
    print("\n" + "="*70)
    print("Example 7: Error Handling with Error Objects")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # Try to add rows to a non-existent sheet
        invalid_sheet_id = 999999999999
        
        row = Row()
        row.to_bottom = True
        row.cells = [Cell({'column_id': 123, 'value': 'Test'})]
        
        print(f"Attempting to add rows to invalid sheet {invalid_sheet_id}...")
        result = await client.Sheets.add_rows(invalid_sheet_id, [row])
        
        # Check if result is an Error object
        if isinstance(result, Error):
            print(f"✓ Error detected (as expected):")
            print(f"  Status Code: {result.result.status_code}")
            print(f"  Error Code: {result.result.code}")
            print(f"  Message: {result.result.message}")
            print(f"  Should Retry: {result.result.should_retry}")
            print(f"  Recommendation: {result.result.recommendation}")
            
            if hasattr(result.result, 'ref_id') and result.result.ref_id:
                print(f"  Reference ID: {result.result.ref_id}")
        else:
            print(f"✗ Unexpected success: {result.message}")


# =============================================================================
# Example 8: Error Handling with Exceptions
# =============================================================================

async def example_error_handling_exceptions():
    """
    Demonstrates error handling using exceptions.
    
    You can configure the client to raise exceptions instead of returning
    Error objects by calling errors_as_exceptions(True).
    """
    print("\n" + "="*70)
    print("Example 8: Error Handling with Exceptions")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    async with AsyncSmartsheet(access_token=access_token) as client:
        # Enable exception raising
        client.errors_as_exceptions(True)
        print("✓ Configured client to raise exceptions")
        
        # Try to add rows to a non-existent sheet
        invalid_sheet_id = 999999999999
        
        row = Row()
        row.to_bottom = True
        row.cells = [Cell({'column_id': 123, 'value': 'Test'})]
        
        print(f"Attempting to add rows to invalid sheet {invalid_sheet_id}...")
        
        try:
            result = await client.Sheets.add_rows(invalid_sheet_id, [row])
            print(f"✗ Unexpected success: {result.message}")
        except Exception as e:
            print(f"✓ Exception caught (as expected):")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Message: {str(e)}")
            
            # Access error details if available
            if hasattr(e, 'error'):
                print(f"  Error Code: {e.error.result.code}")
                print(f"  Status Code: {e.error.result.status_code}")


# =============================================================================
# Example 9: Async Service Integration Pattern
# =============================================================================

async def example_async_service_pattern():
    """
    Demonstrates the pattern for integrating with async services.
    
    This shows how to create a reusable client instance for async service handlers.
    Note: This is a demonstration of the pattern, works with any async framework.
    """
    print("\n" + "="*70)
    print("Example 9: Async Service Integration Pattern")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    # In a real async service, you would create this at module level
    # and reuse it across multiple handler invocations
    global_client = None
    
    async def get_client():
        """Get or create the Smartsheet client."""
        nonlocal global_client
        if global_client is None:
            global_client = AsyncSmartsheet(access_token=access_token)
            print("✓ Created global client instance")
        return global_client
    
    # Simulate multiple service handler calls
    print("\nSimulating async service handler call 1...")
    client = await get_client()
    result1 = await client.Workspaces.list_workspaces()
    if not isinstance(result1, Error):
        print(f"✓ Handler 1: Found {len(result1.data)} workspaces")
    
    print("\nSimulating async service handler call 2...")
    client = await get_client()  # Reuses same client
    result2 = await client.Workspaces.list_workspaces()
    if not isinstance(result2, Error):
        print(f"✓ Handler 2: Found {len(result2.data)} workspaces")
    
    # Cleanup (would be done in service shutdown handler)
    if global_client:
        await global_client.aclose()
        print("\n✓ Cleaned up global client")


# =============================================================================
# Example 10: Configuration Options
# =============================================================================

async def example_configuration_options():
    """
    Demonstrates various configuration options for the async client.
    """
    print("\n" + "="*70)
    print("Example 10: Configuration Options")
    print("="*70)
    
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("⚠️  SMARTSHEET_ACCESS_TOKEN not set. Skipping example.")
        return
    
    # Create client with custom configuration
    async with AsyncSmartsheet(
        access_token=access_token,
        max_connections=10,          # Increase max concurrent connections
        max_retry_time=60,           # Retry for up to 60 seconds
        user_agent="MyApp/1.0",      # Custom user agent
        # proxies={"https": "..."},  # Uncomment to use proxy
    ) as client:
        print("✓ Client initialized with custom configuration:")
        print("  - max_connections: 10")
        print("  - max_retry_time: 60 seconds")
        print("  - user_agent: MyApp/1.0")
        
        # Test the configured client
        result = await client.Workspaces.list_workspaces()
        
        if not isinstance(result, Error):
            print(f"\n✓ Successfully listed {len(result.data)} workspaces")


# =============================================================================
# Main Function - Run All Examples
# =============================================================================

async def main():
    """
    Run all examples.
    
    Note: Some examples require specific sheet IDs and column IDs.
    Modify the values below to match your Smartsheet environment.
    """
    print("\n" + "="*70)
    print("Smartsheet Python SDK - Async Examples")
    print("="*70)
    
    # Check for access token
    access_token = os.environ.get('SMARTSHEET_ACCESS_TOKEN')
    if not access_token:
        print("\n⚠️  WARNING: SMARTSHEET_ACCESS_TOKEN environment variable not set!")
        print("Set it with: export SMARTSHEET_ACCESS_TOKEN='your_token_here'")
        print("\nRunning examples in demo mode (will show errors)...\n")
    
    # Run basic examples (don't require specific IDs)
    await example_basic_usage()
    await example_manual_cleanup()
    await example_list_workspaces_pagination()
    await example_error_handling_objects()
    await example_error_handling_exceptions()
    await example_async_service_pattern()
    await example_configuration_options()
    
    # Examples that require specific sheet/column IDs
    # Uncomment and modify these to run with your actual data
    
    # SHEET_ID = 1234567890  # Replace with your sheet ID
    # COLUMN_IDS = [111, 222, 333]  # Replace with your column IDs
    # 
    # await example_add_rows(SHEET_ID, COLUMN_IDS)
    # await example_concurrent_operations([SHEET_ID], COLUMN_IDS)
    # await example_mixed_concurrent_operations(SHEET_ID, COLUMN_IDS)
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)
    print("\nTo run examples that modify sheets, uncomment and configure")
    print("the sheet ID and column ID variables in the main() function.")
    print("\nFor more information, see:")
    print("  - docs-source/async-quickstart.md")
    print("  - https://smartsheet.github.io/smartsheet-python-sdk/")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
