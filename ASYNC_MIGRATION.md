# Async Migration Guide

This guide helps you migrate from the synchronous Smartsheet Python SDK to the new async implementation. Whether you're building a new async application or converting existing code, this guide provides practical examples and best practices.

## Table of Contents

- [Why Migrate to Async?](#why-migrate-to-async)
- [Prerequisites](#prerequisites)
- [Quick Migration Checklist](#quick-migration-checklist)
- [Side-by-Side Comparisons](#side-by-side-comparisons)
- [Common Patterns](#common-patterns)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Why Migrate to Async?

Consider migrating to async if your application:

- **Makes multiple concurrent API calls** - Async can significantly reduce total execution time
- **Integrates with async frameworks** - FastAPI, aiohttp, and other async services
- **Handles high throughput** - Process many sheets or workspaces efficiently
- **Needs non-blocking I/O** - Keep your application responsive during API calls
- **Runs in an async environment** - Already using asyncio event loop

**Don't migrate if:**

- Your application makes sequential API calls only
- You're satisfied with current performance
- Your codebase doesn't support async/await patterns
- You're not familiar with async Python programming

## Prerequisites

### 1. Install Required Dependencies

```bash
pip install smartsheet-python-sdk httpx
```

### 2. Python Version

Async support requires Python 3.7 or higher (same as the sync SDK).

### 3. Understanding Async/Await

Familiarize yourself with Python's async/await syntax:

- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python async tutorial](https://realpython.com/async-io-python/)

## Quick Migration Checklist

Use this checklist when converting code:

- [ ] Install `httpx` dependency
- [ ] Change `import smartsheet` to `from smartsheet import AsyncSmartsheet`
- [ ] Change `Smartsheet()` to `AsyncSmartsheet()`
- [ ] Add `async` keyword to function definitions
- [ ] Add `await` before all API method calls
- [ ] Change `with` to `async with` for context managers
- [ ] Replace `client.close()` with `await client.aclose()`
- [ ] Wrap execution in `asyncio.run()` if running from main script
- [ ] Update error handling if needed
- [ ] Test thoroughly with your use cases

## Side-by-Side Comparisons

### Basic Client Usage

#### Synchronous (Before)

```python
import smartsheet

# Create client
client = smartsheet.Smartsheet(access_token="your_token")

# Use client
workspaces = client.Workspaces.list_workspaces()
print(f"Found {len(workspaces.data)} workspaces")

# No explicit cleanup needed
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    # Create client with context manager
    async with AsyncSmartsheet(access_token="your_token") as client:
        # Use client with await
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")
    # Automatic cleanup

# Run async function
asyncio.run(main())
```

### Listing Workspaces

#### Synchronous (Before)

```python
import smartsheet

client = smartsheet.Smartsheet(access_token="your_token")

# Legacy pagination
result = client.Workspaces.list_workspaces(page_size=100, page=1)

for workspace in result.data:
    print(f"{workspace.name}: {workspace.id}")
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        # Token pagination (recommended)
        result = await client.Workspaces.list_workspaces(
            pagination_type='token',
            max_items=100
        )
        
        for workspace in result.data:
            print(f"{workspace.name}: {workspace.id}")

asyncio.run(main())
```

### Adding Rows to a Sheet

#### Synchronous (Before)

```python
import smartsheet
from smartsheet.models import Row, Cell

client = smartsheet.Smartsheet(access_token="your_token")

# Create row
row = Row()
row.to_bottom = True
row.cells = [
    Cell({'column_id': 123456, 'value': 'Task Name'}),
    Cell({'column_id': 789012, 'value': 'In Progress'})
]

# Add row
result = client.Sheets.add_rows(sheet_id=111222, list_of_rows=[row])

if result.message == 'SUCCESS':
    print(f"Added row {result.data[0].id}")
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        # Create row (same as sync)
        row = Row()
        row.to_bottom = True
        row.cells = [
            Cell({'column_id': 123456, 'value': 'Task Name'}),
            Cell({'column_id': 789012, 'value': 'In Progress'})
        ]
        
        # Add row with await
        result = await client.Sheets.add_rows(sheet_id=111222, list_of_rows=[row])
        
        if result.message == 'SUCCESS':
            print(f"Added row {result.data[0].id}")

asyncio.run(main())
```

### Error Handling

#### Synchronous (Before)

```python
import smartsheet
from smartsheet.models import Error

client = smartsheet.Smartsheet(access_token="your_token")

result = client.Workspaces.list_workspaces()

if isinstance(result, Error):
    print(f"Error: {result.result.message}")
else:
    print(f"Success: {len(result.data)} workspaces")
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.models import Error

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        result = await client.Workspaces.list_workspaces()
        
        if isinstance(result, Error):
            print(f"Error: {result.result.message}")
        else:
            print(f"Success: {len(result.data)} workspaces")

asyncio.run(main())
```

### Exception-Based Error Handling

#### Synchronous (Before)

```python
import smartsheet
from smartsheet.exceptions import ApiError

client = smartsheet.Smartsheet(access_token="your_token")
client.errors_as_exceptions(True)

try:
    result = client.Workspaces.list_workspaces()
    print(f"Found {len(result.data)} workspaces")
except ApiError as e:
    print(f"API Error: {e}")
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet
from smartsheet.exceptions import ApiError

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        client.errors_as_exceptions(True)
        
        try:
            result = await client.Workspaces.list_workspaces()
            print(f"Found {len(result.data)} workspaces")
        except ApiError as e:
            print(f"API Error: {e}")

asyncio.run(main())
```

## Common Patterns

### Pattern 1: Sequential Operations

When operations must happen in sequence:

#### Synchronous (Before)

```python
import smartsheet

client = smartsheet.Smartsheet(access_token="your_token")

# Sequential operations
workspaces = client.Workspaces.list_workspaces()
print(f"Step 1: Found {len(workspaces.data)} workspaces")

result = client.Sheets.add_rows(sheet_id, rows)
print(f"Step 2: Added {len(result.data)} rows")
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        # Sequential operations (still use await)
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Step 1: Found {len(workspaces.data)} workspaces")
        
        result = await client.Sheets.add_rows(sheet_id, rows)
        print(f"Step 2: Added {len(result.data)} rows")

asyncio.run(main())
```

### Pattern 2: Concurrent Operations (New Capability!)

One of the main benefits of async - operations that can run concurrently:

#### Synchronous (Before) - Sequential Only

```python
import smartsheet
import time

client = smartsheet.Smartsheet(access_token="your_token")

start = time.time()

# Must run sequentially
result1 = client.Sheets.add_rows(sheet_id_1, rows)
result2 = client.Sheets.add_rows(sheet_id_2, rows)
result3 = client.Sheets.add_rows(sheet_id_3, rows)

elapsed = time.time() - start
print(f"Completed in {elapsed:.2f} seconds")
```

#### Asynchronous (After) - Concurrent

```python
import asyncio
import time
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        start = time.time()
        
        # Run concurrently - much faster!
        results = await asyncio.gather(
            client.Sheets.add_rows(sheet_id_1, rows),
            client.Sheets.add_rows(sheet_id_2, rows),
            client.Sheets.add_rows(sheet_id_3, rows)
        )
        
        elapsed = time.time() - start
        print(f"Completed in {elapsed:.2f} seconds")  # Significantly faster!

asyncio.run(main())
```

### Pattern 3: Processing Multiple Items

#### Synchronous (Before)

```python
import smartsheet

client = smartsheet.Smartsheet(access_token="your_token")

sheet_ids = [111, 222, 333, 444, 555]

for sheet_id in sheet_ids:
    result = client.Sheets.add_rows(sheet_id, rows)
    print(f"Processed sheet {sheet_id}")
```

#### Asynchronous (After) - With Concurrency

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token") as client:
        sheet_ids = [111, 222, 333, 444, 555]
        
        # Process all sheets concurrently
        tasks = [
            client.Sheets.add_rows(sheet_id, rows)
            for sheet_id in sheet_ids
        ]
        
        results = await asyncio.gather(*tasks)
        
        for sheet_id, result in zip(sheet_ids, results):
            print(f"Processed sheet {sheet_id}")

asyncio.run(main())
```

### Pattern 4: Reusable Client in a Class

#### Synchronous (Before)

```python
import smartsheet

class SmartsheetService:
    def __init__(self, access_token):
        self.client = smartsheet.Smartsheet(access_token=access_token)
    
    def get_workspaces(self):
        return self.client.Workspaces.list_workspaces()
    
    def add_row(self, sheet_id, row):
        return self.client.Sheets.add_rows(sheet_id, [row])

# Usage
service = SmartsheetService("your_token")
workspaces = service.get_workspaces()
```

#### Asynchronous (After)

```python
import asyncio
from smartsheet import AsyncSmartsheet

class AsyncSmartsheetService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = None
    
    async def __aenter__(self):
        self.client = AsyncSmartsheet(access_token=self.access_token)
        await self.client._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
        return False
    
    async def get_workspaces(self):
        return await self.client.Workspaces.list_workspaces()
    
    async def add_row(self, sheet_id, row):
        return await self.client.Sheets.add_rows(sheet_id, [row])

# Usage
async def main():
    async with AsyncSmartsheetService("your_token") as service:
        workspaces = await service.get_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")

asyncio.run(main())
```

### Pattern 5: Async Service Integration

#### New Pattern - Async Only

```python
from smartsheet import AsyncSmartsheet
from smartsheet.models import Row, Cell

# Example async service pattern
# (Works with any async framework)

# Global client instance
smartsheet_client = None

async def get_client():
    """Get or create the Smartsheet client."""
    global smartsheet_client
    if smartsheet_client is None:
        smartsheet_client = AsyncSmartsheet(access_token="your_token")
    return smartsheet_client

@mcp.tool()
async def list_workspaces() -> list[dict]:
    """List all Smartsheet workspaces."""
    client = await get_client()
    result = await client.Workspaces.list_workspaces(
        pagination_type='token',
        max_items=100
    )
    
    return [
        {"id": ws.id, "name": ws.name, "access_level": ws.access_level}
        for ws in result.data
    ]

@mcp.tool()
async def add_sheet_row(sheet_id: int, column_values: dict[int, str]) -> str:
    """Add a row to a Smartsheet."""
    client = await get_client()
    
    row = Row()
    row.to_bottom = True
    row.cells = [
        Cell({'column_id': col_id, 'value': value})
        for col_id, value in column_values.items()
    ]
    
    result = await client.Sheets.add_rows(sheet_id, [row])
    
    if result.message == 'SUCCESS':
        return f"Added row {result.data[0].id}"
    else:
        return f"Error: {result.message}"

@mcp.on_shutdown
async def cleanup():
    """Clean up resources on shutdown."""
    global smartsheet_client
    if smartsheet_client:
        await smartsheet_client.aclose()
```

## Performance Considerations

### When Async Provides Benefits

**Significant Performance Gains:**

```python
# Adding rows to 10 sheets
# Sync: ~10 seconds (sequential)
# Async: ~1-2 seconds (concurrent)

async def concurrent_example():
    async with AsyncSmartsheet(access_token="token") as client:
        tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids]
        results = await asyncio.gather(*tasks)  # Much faster!
```

**Minimal Performance Difference:**

```python
# Single operation
# Sync: ~1 second
# Async: ~1 second (no concurrency benefit)

async def single_operation():
    async with AsyncSmartsheet(access_token="token") as client:
        result = await client.Workspaces.list_workspaces()  # Same speed as sync
```

### Overhead Considerations

- **Client initialization**: Slightly more overhead for async client setup
- **Single operations**: No performance benefit over sync
- **Memory usage**: Async may use slightly more memory for event loop
- **Complexity**: Async code is more complex to write and debug

### Optimization Tips

1. **Batch concurrent operations** - Group related API calls together
2. **Limit concurrency** - Don't overwhelm the API with too many concurrent requests
3. **Reuse client instances** - Create one client and reuse it
4. **Use token pagination** - More efficient than legacy pagination
5. **Monitor rate limits** - The client handles retries, but be aware of limits

## Troubleshooting

### Issue: "RuntimeError: Event loop is closed"

**Cause**: Trying to run async code in an environment with a closed event loop.

**Solution**:

```python
# In scripts, use asyncio.run()
asyncio.run(main())

# In Jupyter/IPython, await directly
await main()

# In existing async context, just await
result = await client.Workspaces.list_workspaces()
```

### Issue: "ModuleNotFoundError: No module named 'httpx'"

**Cause**: Missing httpx dependency.

**Solution**:

```bash
pip install httpx
```

### Issue: "AttributeError: 'AsyncSmartsheet' object has no attribute 'X'"

**Cause**: Trying to use an API method that hasn't been implemented in async yet.

**Solution**: Check the [PoC scope](docs-source/async-quickstart.md#current-status-proof-of-concept-poc). Currently only `add_rows` and `list_workspaces` are supported. Use the sync client for other operations or request the feature.

### Issue: Slower than expected performance

**Cause**: Not using concurrent operations, or hitting rate limits.

**Solution**:

```python
# Bad - sequential (no benefit)
for sheet_id in sheet_ids:
    result = await client.Sheets.add_rows(sheet_id, rows)

# Good - concurrent (much faster)
tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids]
results = await asyncio.gather(*tasks)
```

### Issue: "Session is None" errors

**Cause**: Not properly initializing the client.

**Solution**: Always use `async with` or manually call `await client._ensure_session()`:

```python
# Recommended
async with AsyncSmartsheet(access_token="token") as client:
    result = await client.Workspaces.list_workspaces()

# Or manual initialization
client = AsyncSmartsheet(access_token="token")
await client._ensure_session()
try:
    result = await client.Workspaces.list_workspaces()
finally:
    await client.aclose()
```

### Issue: Rate limiting errors

**Cause**: Too many concurrent requests.

**Solution**: Limit concurrency or increase retry time:

```python
# Limit concurrent operations
from asyncio import Semaphore

async def limited_concurrency():
    async with AsyncSmartsheet(access_token="token") as client:
        semaphore = Semaphore(5)  # Max 5 concurrent operations
        
        async def add_with_limit(sheet_id):
            async with semaphore:
                return await client.Sheets.add_rows(sheet_id, rows)
        
        tasks = [add_with_limit(sid) for sid in sheet_ids]
        results = await asyncio.gather(*tasks)

# Or increase retry time
client = AsyncSmartsheet(
    access_token="token",
    max_retry_time=120  # Retry for up to 2 minutes
)
```

## Best Practices

### 1. Always Use Context Managers

```python
# Good
async with AsyncSmartsheet(access_token="token") as client:
    result = await client.Workspaces.list_workspaces()

# Avoid
client = AsyncSmartsheet(access_token="token")
result = await client.Workspaces.list_workspaces()
# Easy to forget: await client.aclose()
```

### 2. Reuse Client Instances

```python
# Good - one client for multiple operations
async with AsyncSmartsheet(access_token="token") as client:
    ws = await client.Workspaces.list_workspaces()
    r1 = await client.Sheets.add_rows(sheet1, rows)
    r2 = await client.Sheets.add_rows(sheet2, rows)

# Avoid - creating multiple clients
async with AsyncSmartsheet(access_token="token") as c1:
    ws = await c1.Workspaces.list_workspaces()
async with AsyncSmartsheet(access_token="token") as c2:
    r1 = await c2.Sheets.add_rows(sheet1, rows)
```

### 3. Use Concurrent Operations Wisely

```python
# Good - reasonable concurrency
tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids[:10]]
results = await asyncio.gather(*tasks)

# Be careful - may hit rate limits
tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids[:1000]]
results = await asyncio.gather(*tasks)  # Too many concurrent requests
```

### 4. Handle Errors Appropriately

```python
# For fine-grained error handling
result = await client.Workspaces.list_workspaces()
if isinstance(result, Error):
    # Handle error
    pass

# For exception-based flow
client.errors_as_exceptions(True)
try:
    result = await client.Workspaces.list_workspaces()
except ApiError as e:
    # Handle exception
    pass
```

### 5. Test Thoroughly

- Test with real API calls in a development environment
- Test error scenarios (invalid IDs, rate limits, etc.)
- Test concurrent operations with your actual workload
- Monitor performance and adjust concurrency as needed

### 6. Document Async Functions

```python
async def process_sheets(sheet_ids: list[int]) -> list[Result]:
    """Process multiple sheets concurrently.
    
    Args:
        sheet_ids: List of sheet IDs to process
        
    Returns:
        List of results from each sheet operation
        
    Note:
        This is an async function and must be awaited.
    """
    async with AsyncSmartsheet(access_token="token") as client:
        tasks = [client.Sheets.add_rows(sid, rows) for sid in sheet_ids]
        return await asyncio.gather(*tasks)
```

## Migration Strategy

### Incremental Migration

You can use both sync and async clients in the same application:

```python
import smartsheet
from smartsheet import AsyncSmartsheet
import asyncio

# Sync client for existing code
sync_client = smartsheet.Smartsheet(access_token="token")
workspaces = sync_client.Workspaces.list_workspaces()

# Async client for new code
async def new_feature():
    async with AsyncSmartsheet(access_token="token") as async_client:
        result = await async_client.Sheets.add_rows(sheet_id, rows)
    return result

# Call async from sync context
result = asyncio.run(new_feature())
```

### Full Migration Steps

1. **Start with non-critical code** - Migrate less critical features first
2. **Test thoroughly** - Ensure async version works correctly
3. **Measure performance** - Verify you're getting expected benefits
4. **Migrate incrementally** - Don't try to migrate everything at once
5. **Update documentation** - Document which parts are async
6. **Train team** - Ensure team understands async patterns

## Additional Resources

- [Async Quick Start Guide](docs-source/async-quickstart.md)
- [Example Code](examples/async_examples.py)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python Async Tutorial](https://realpython.com/async-io-python/)
- [GitHub Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues)

## Getting Help

If you encounter issues during migration:

1. Check this guide and the [troubleshooting section](#troubleshooting)
2. Review the [async quickstart guide](docs-source/async-quickstart.md)
3. Look at the [example code](examples/async_examples.py)
4. Search [GitHub Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues)
5. Create a new issue with details about your use case

We welcome feedback on the async implementation and this migration guide!
