# Async Support Quick Start Guide

## Overview

The Smartsheet Python SDK now includes **beta async support** for non-blocking I/O operations. This allows you to write more efficient applications that can handle multiple Smartsheet API requests concurrently, particularly useful for:

- **Async frameworks** and event loop-based applications
- High-throughput applications processing multiple sheets
- Applications that need to make concurrent API calls
- Integration with modern async Python frameworks (FastAPI, aiohttp, etc.)

### Why Async?

Traditional synchronous API calls block execution while waiting for network responses. With async support, your application can:

- Make multiple API requests concurrently
- Improve throughput and reduce total execution time
- Integrate seamlessly with async frameworks
- Better utilize system resources

### Current Status: Proof of Concept (PoC)

This is a **beta/PoC implementation** with limited scope. Currently supported operations:

- ✅ **Sheets.add_rows()** - Add rows to a sheet
- ✅ **Workspaces.list_workspaces()** - List workspaces

Additional async operations will be added based on user feedback and demand.

## Installation

The async client requires the `httpx` library for async HTTP operations:

```bash
pip install smartsheet-python-sdk httpx
```

Or if you're installing from source:

```bash
pip install smartsheet-python-sdk[async]
```

## Basic Usage

### Using Async Context Manager (Recommended)

The recommended way to use the async client is with an async context manager, which automatically handles resource cleanup:

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # List workspaces
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")
        
        for workspace in workspaces.data:
            print(f"  - {workspace.name}")

# Run the async function
asyncio.run(main())
```

### Manual Resource Management

If you need more control over the client lifecycle, you can manually manage resources:

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    client = AsyncSmartsheet(access_token="your_token_here")
    try:
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")
    finally:
        # Always close the client to release resources
        await client.aclose()

asyncio.run(main())
```

**Important:** Always call `await client.aclose()` when done to properly release HTTP connections and resources.

## PoC Scope Examples

### Adding Rows to a Sheet

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

async def add_rows_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # Create rows to add
        row1 = Row()
        row1.to_bottom = True
        row1.cells = [
            Cell({'column_id': 123456789, 'value': 'New Task'}),
            Cell({'column_id': 987654321, 'value': 'In Progress'}),
            Cell({'column_id': 555555555, 'value': 'High'})
        ]
        
        row2 = Row()
        row2.to_bottom = True
        row2.cells = [
            Cell({'column_id': 123456789, 'value': 'Another Task'}),
            Cell({'column_id': 987654321, 'value': 'Not Started'}),
            Cell({'column_id': 555555555, 'value': 'Medium'})
        ]
        
        # Add rows asynchronously
        sheet_id = 1234567890
        result = await client.Sheets.add_rows(sheet_id, [row1, row2])
        
        if result.message == 'SUCCESS':
            print(f"Successfully added {len(result.data)} rows")
            for row in result.data:
                print(f"  Row ID: {row.id}, Row Number: {row.row_number}")
        else:
            print(f"Error: {result.message}")

asyncio.run(add_rows_example())
```

### Listing Workspaces with Token Pagination

Token-based pagination is more efficient than legacy offset-based pagination:

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def list_workspaces_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # First page
        result = await client.Workspaces.list_workspaces(
            pagination_type='token',
            max_items=100
        )
        
        print(f"Found {len(result.data)} workspaces on first page")
        for workspace in result.data:
            print(f"  - {workspace.name} (ID: {workspace.id})")
        
        # Check if there are more pages
        if hasattr(result, 'next_token') and result.next_token:
            print(f"\nFetching next page...")
            next_result = await client.Workspaces.list_workspaces(
                pagination_type='token',
                last_key=result.next_token,
                max_items=100
            )
            print(f"Found {len(next_result.data)} workspaces on second page")

asyncio.run(list_workspaces_example())
```

## Async Framework Integration

The async client integrates seamlessly with async frameworks and event loop-based applications:

```python
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

# Example: Async service pattern
# (This pattern works with any async framework)

# Initialize async client (reuse across requests)
smartsheet_client = None

async def get_client():
    """Get or create the Smartsheet client."""
    global smartsheet_client
    if smartsheet_client is None:
        smartsheet_client = AsyncSmartsheet(access_token="your_token_here")
    return smartsheet_client

async def add_sheet_row(
    sheet_id: int,
    column_values: dict[int, str]
) -> str:
    """Add a row to a Smartsheet.
    
    Args:
        sheet_id: The ID of the sheet
        column_values: Dictionary mapping column IDs to values
    
    Returns:
        Success message with row details
    """
    client = await get_client()
    
    # Create row
    row = Row()
    row.to_bottom = True
    row.cells = [
        Cell({'column_id': col_id, 'value': value})
        for col_id, value in column_values.items()
    ]
    
    # Add row
    result = await client.Sheets.add_rows(sheet_id, [row])
    
    if result.message == 'SUCCESS':
        return f"Added row {result.data[0].id} to sheet {sheet_id}"
    else:
        return f"Error: {result.message}"

async def list_workspaces() -> list[dict]:
    """List all Smartsheet workspaces.
    
    Returns:
        List of workspace information
    """
    client = await get_client()
    
    result = await client.Workspaces.list_workspaces(
        pagination_type='token',
        max_items=100
    )
    
    return [
        {
            "id": ws.id,
            "name": ws.name,
            "access_level": ws.access_level
        }
        for ws in result.data
    ]

# Cleanup on shutdown
async def cleanup():
    """Clean up resources on shutdown."""
    global smartsheet_client
    if smartsheet_client:
        await smartsheet_client.aclose()
```

## Concurrent Operations

One of the main benefits of async is the ability to run multiple operations concurrently:

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

async def concurrent_operations_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # Create rows for different sheets
        row = Row()
        row.to_bottom = True
        row.cells = [
            Cell({'column_id': 123456789, 'value': 'Concurrent Task'})
        ]
        
        # Execute multiple add_rows operations concurrently
        sheet_ids = [111111, 222222, 333333, 444444, 555555]
        
        tasks = [
            client.Sheets.add_rows(sheet_id, [row])
            for sheet_id in sheet_ids
        ]
        
        # Wait for all operations to complete
        results = await asyncio.gather(*tasks)
        
        # Process results
        for sheet_id, result in zip(sheet_ids, results):
            if result.message == 'SUCCESS':
                print(f"✓ Sheet {sheet_id}: Added {len(result.data)} rows")
            else:
                print(f"✗ Sheet {sheet_id}: Error - {result.message}")

asyncio.run(concurrent_operations_example())
```

### Mixed Concurrent Operations

You can also mix different types of operations:

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

async def mixed_operations_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        row = Row()
        row.to_bottom = True
        row.cells = [Cell({'column_id': 123456789, 'value': 'Data'})]
        
        # Run different operations concurrently
        results = await asyncio.gather(
            client.Workspaces.list_workspaces(),
            client.Sheets.add_rows(111111, [row]),
            client.Sheets.add_rows(222222, [row]),
            client.Workspaces.list_workspaces(pagination_type='token', max_items=50)
        )
        
        workspaces1, add_result1, add_result2, workspaces2 = results
        
        print(f"Found {len(workspaces1.data)} workspaces")
        print(f"Added rows to 2 sheets")
        print(f"Found {len(workspaces2.data)} workspaces (token pagination)")

asyncio.run(mixed_operations_example())
```

## Error Handling

### Default Error Handling (Return Error Objects)

By default, the async client returns `Error` objects instead of raising exceptions:

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Error

async def error_handling_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        result = await client.Sheets.add_rows(999999, [])  # Invalid sheet ID
        
        if isinstance(result, Error):
            print(f"Error occurred:")
            print(f"  Status Code: {result.result.status_code}")
            print(f"  Error Code: {result.result.code}")
            print(f"  Message: {result.result.message}")
            print(f"  Should Retry: {result.result.should_retry}")
        else:
            print(f"Success: {result.message}")

asyncio.run(error_handling_example())
```

### Exception-Based Error Handling

You can configure the client to raise exceptions instead:

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.exceptions import ApiError

async def exception_handling_example():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # Enable exception raising
        client.errors_as_exceptions(True)
        
        try:
            result = await client.Sheets.add_rows(999999, [])
        except ApiError as e:
            print(f"API Error: {e}")
            print(f"Error details: {e.error.result.message}")

asyncio.run(exception_handling_example())
```

### Handling Rate Limits

The async client automatically retries on rate limit errors (429):

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def rate_limit_example():
    async with AsyncSmartsheet(
        access_token="your_token_here",
        max_retry_time=60  # Retry for up to 60 seconds
    ) as client:
        # The client will automatically retry if rate limited
        result = await client.Workspaces.list_workspaces()
        print(f"Found {len(result.data)} workspaces")

asyncio.run(rate_limit_example())
```

## Migration Guide from Sync to Async

### Basic Conversion

**Synchronous Code:**

```python
import smartsheet

client = smartsheet.Smartsheet(access_token="token")
workspaces = client.Workspaces.list_workspaces()
print(f"Found {len(workspaces.data)} workspaces")
```

**Async Code:**

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="token") as client:
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")

asyncio.run(main())
```

### Key Differences

1. **Import**: Use `AsyncSmartsheet` instead of `Smartsheet`
2. **Async Functions**: All functions that call the API must be `async`
3. **Await Calls**: Use `await` before API method calls
4. **Context Manager**: Use `async with` instead of regular `with`
5. **Resource Cleanup**: Call `await client.aclose()` or use context manager
6. **Running**: Use `asyncio.run()` to execute async functions

### Migration Checklist

- [ ] Change `import smartsheet` to `from smartsheet import AsyncSmartsheet`
- [ ] Change `Smartsheet()` to `AsyncSmartsheet()`
- [ ] Add `async` keyword to function definitions
- [ ] Add `await` before all API method calls
- [ ] Use `async with` for context managers
- [ ] Call `await client.aclose()` if not using context manager
- [ ] Wrap execution in `asyncio.run()` if running from main script
- [ ] Install `httpx` dependency

## Configuration Options

The `AsyncSmartsheet` client accepts the same configuration options as the sync client:

```python
from smartsheet import AsyncSmartsheet

client = AsyncSmartsheet(
    access_token="your_token_here",
    max_connections=8,           # Max concurrent connections (default: 8)
    max_retry_time=30,           # Max retry time in seconds (default: 30)
    user_agent="MyApp/1.0",      # Custom user agent
    proxies={"https": "..."},    # Proxy configuration
    api_base="https://api.smartsheet.com/2.0"  # API base URL
)
```

## Limitations and Future Roadmap

### Current Limitations (PoC)

- **Limited API Coverage**: Only `add_rows` and `list_workspaces` are currently supported
- **Beta Status**: API may change based on feedback
- **Testing**: While comprehensive tests exist, real-world usage may reveal edge cases

### Planned Future Enhancements

Based on user feedback, we plan to add:

1. **More Sheet Operations**
   - `get_sheet()` - Retrieve sheet data
   - `update_rows()` - Update existing rows
   - `delete_rows()` - Delete rows
   - `get_columns()` - Get column information

2. **Additional Resources**
   - Full Workspaces API support
   - Folders operations
   - Reports operations
   - Attachments operations

3. **Advanced Features**
   - Batch operations optimization
   - Connection pooling improvements
   - Streaming support for large datasets

### Providing Feedback

We welcome feedback on the async implementation! Please:

- Report issues on [GitHub Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues)
- Share your use cases and requirements
- Suggest which operations should be prioritized for async support

## Best Practices

### 1. Use Context Managers

Always use `async with` to ensure proper resource cleanup:

```python
# Good
async with AsyncSmartsheet(access_token="token") as client:
    result = await client.Workspaces.list_workspaces()

# Avoid (unless you have a specific reason)
client = AsyncSmartsheet(access_token="token")
result = await client.Workspaces.list_workspaces()
# Easy to forget: await client.aclose()
```

### 2. Reuse Client Instances

Create one client instance and reuse it across multiple operations:

```python
# Good - reuse client
async with AsyncSmartsheet(access_token="token") as client:
    result1 = await client.Workspaces.list_workspaces()
    result2 = await client.Sheets.add_rows(sheet_id, rows)

# Avoid - creating multiple clients
async with AsyncSmartsheet(access_token="token") as client1:
    result1 = await client1.Workspaces.list_workspaces()

async with AsyncSmartsheet(access_token="token") as client2:
    result2 = await client2.Sheets.add_rows(sheet_id, rows)
```

### 3. Use Concurrent Operations Wisely

Take advantage of async for concurrent operations, but be mindful of rate limits:

```python
# Good - reasonable concurrency
tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids[:10]]
results = await asyncio.gather(*tasks)

# Be careful - too many concurrent requests may hit rate limits
tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids[:1000]]
results = await asyncio.gather(*tasks)  # May trigger rate limiting
```

### 4. Handle Errors Appropriately

Choose the error handling style that fits your application:

```python
# For applications that need fine-grained error handling
result = await client.Workspaces.list_workspaces()
if isinstance(result, Error):
    # Handle error
    pass

# For applications that prefer exceptions
client.errors_as_exceptions(True)
try:
    result = await client.Workspaces.list_workspaces()
except ApiError as e:
    # Handle exception
    pass
```

### 5. Configure Retry Behavior

Adjust retry settings based on your application's needs:

```python
# For time-sensitive operations
client = AsyncSmartsheet(
    access_token="token",
    max_retry_time=10  # Give up after 10 seconds
)

# For batch operations that can tolerate delays
client = AsyncSmartsheet(
    access_token="token",
    max_retry_time=120  # Retry for up to 2 minutes
)
```

## Troubleshooting

### "RuntimeError: Event loop is closed"

This usually happens when trying to run async code in an environment that already has an event loop. Use `asyncio.run()` only in scripts, not in Jupyter notebooks or frameworks with existing event loops.

**Solution for Jupyter/IPython:**

```python
# Instead of asyncio.run(main())
await main()  # In Jupyter, you can await directly
```

### "httpx not installed"

The async client requires httpx. Install it:

```bash
pip install httpx
```

### "Session is None" errors

Make sure you're using the client correctly:

```python
# Wrong - session not initialized
client = AsyncSmartsheet(access_token="token")
result = await client.Workspaces.list_workspaces()  # May fail

# Correct - use context manager
async with AsyncSmartsheet(access_token="token") as client:
    result = await client.Workspaces.list_workspaces()  # Works
```

### Rate Limiting Issues

If you're hitting rate limits frequently:

1. Reduce concurrency
2. Increase `max_retry_time`
3. Add delays between batches of requests
4. Consider using the sync client for sequential operations

## Additional Resources

- [Full SDK Documentation](https://smartsheet.github.io/smartsheet-python-sdk/)
- [Smartsheet API Documentation](https://developers.smartsheet.com/api/smartsheet/)
- [Async Design Document](async-design.md)
- [GitHub Repository](https://github.com/smartsheet/smartsheet-python-sdk)
- [Example Code](../examples/async_examples.py)

## Support

For questions and support:

- GitHub Issues: [smartsheet-python-sdk/issues](https://github.com/smartsheet/smartsheet-python-sdk/issues)
- Developer Community: [Smartsheet Community](https://community.smartsheet.com/categories/api-developers)
- API Documentation: [developers.smartsheet.com](https://developers.smartsheet.com/)
