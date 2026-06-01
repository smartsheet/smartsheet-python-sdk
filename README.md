# Smartsheet Python SDK

[![Build Status](https://github.com/smartsheet/smartsheet-python-sdk/actions/workflows/test-build.yaml/badge.svg)](https://github.com/smartsheet/smartsheet-python-sdk/actions/workflows/test-build.yaml) [![Coverage Status](https://coveralls.io/repos/github/smartsheet/smartsheet-python-sdk/badge.svg?branch=mainline)](https://coveralls.io/github/smartsheet/smartsheet-python-sdk?branch=mainline) [![PyPI version](https://badge.fury.io/py/smartsheet-python-sdk.svg)](https://badge.fury.io/py/smartsheet-python-sdk)

A library for connecting to the [Smartsheet API](https://developers.smartsheet.com/api/smartsheet/) from Python applications.

## Requirements

The SDK is compatible with [actively supported](https://devguide.python.org/versions/#versions) Python versions `3.10`, `3.9`, `3.8`, `3.7`.

## Installation

To install using [pip](http://www.pip-installer.org/):

```bash
pip install smartsheet-python-sdk
```

## Getting Started

To get started with the Smartsheet Python SDK:

1. Set **SMARTSHEET_ACCESS_TOKEN** in your environment, using your Smartsheet API key. Find out more about [Authentication and Access Tokens](https://developers.smartsheet.com/api/smartsheet/guides/basics/authentication) in the Smartsheet API Documentation. You can generate an access token in Smartsheet UI under Account > Personal Settings > API Access.

2. Install the Smartsheet Python SDK (see the installation instructions above)

3. The following snippet shows how to create a Smartsheet client and perform some basic actions using the SDK. Ensure your Smartsheet user has access to at least one sheet.

``` python

import smartsheet

smart = smartsheet.Smartsheet()             # Create a Smartsheet client

response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
sheetId = response.data[0].id               # Get the ID of the first sheet in the response
sheet = smart.Sheets.get_sheet(sheetId)     # Load the sheet by using its ID

print(f"The sheet {sheet.name} has {sheet.total_row_count} rows")   # Print information about the sheet
```

## Async Support (Beta)

The SDK now includes **beta async support** for non-blocking I/O operations, perfect for async frameworks and high-throughput applications. The async client uses `httpx` for async HTTP operations and provides the same familiar API with async/await patterns.

### Quick Example

```python
import asyncio
from smartsheet import AsyncSmartsheet

async def main():
    async with AsyncSmartsheet(access_token="your_token_here") as client:
        # List workspaces asynchronously
        workspaces = await client.Workspaces.list_workspaces()
        print(f"Found {len(workspaces.data)} workspaces")

        # Add rows to a sheet
        from smartsheet.models import Row, Cell
        row = Row()
        row.to_bottom = True
        row.cells = [Cell({'column_id': 123456, 'value': 'New Value'})]
        result = await client.Sheets.add_rows(sheet_id, [row])
        print(f"Added {len(result.data)} rows")

asyncio.run(main())
```

### Installation

Async support requires the `httpx` library:

```bash
pip install smartsheet-python-sdk httpx
```

### Current PoC Scope

This is a **proof-of-concept** implementation with limited scope:

- ✅ **Sheets.add_rows()** - Add rows to a sheet
- ✅ **Workspaces.list_workspaces()** - List workspaces with token pagination
- ✅ Concurrent operations support
- ✅ Automatic retry with exponential backoff
- ✅ Context manager for resource management

Additional async operations will be added based on user feedback.

### Key Features

- **Non-blocking I/O**: Make multiple API calls concurrently
- **Async Framework Integration**: Perfect for async services and event loop-based applications
- **Familiar API**: Same models and patterns as the sync client
- **Automatic Cleanup**: Use `async with` for automatic resource management

### Learn More

- **[Async Quick Start Guide](docs-source/async-quickstart.md)** - Comprehensive guide with examples
- **[Async Migration Guide](ASYNC_MIGRATION.md)** - How to migrate from sync to async
- **[Example Code](examples/async_examples.py)** - Runnable examples
- **[Design Document](docs-source/async-design.md)** - Technical design details

We welcome feedback on the async implementation! Please share your use cases and requirements via [GitHub Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues).

## Documentation

Use the following resources to learn more about the SDK capabilities:

1. [Smartsheet Python SDK sample project](https://github.com/smartsheet-samples/python-read-write-sheet)
2. [Python SDK documentation](https://smartsheet.github.io/smartsheet-python-sdk/)
3. [Smartsheet API Documentation](https://developers.smartsheet.com/api/smartsheet/)

## Contributing

We welcome contributions! Before submitting code changes, please review our [Issue First approach](ISSUE-FIRST.md) for creating effective issues that work well with both human reviewers and AI-powered Cloud Agents. For additional contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Advanced Topics

For details about logging, testing, how to use a passthrough option, and how to override HTTP client behavior,
see [Advanced Topics](ADVANCED.md).

## Developer Agreement

Review the [Developer Program Agreement](https://www.smartsheet.com/legal/developer-program-agreement).

## Acknowledgements

We would like to thank the following people for their contributions to this project:

- Tim Wells - [timwellswa](https://github.com/timwellswa)
- Scott Wimer - [happybob007](https://github.com/happybob007)
- Steve Weil - [seweil](https://github.com/seweil)
- Kevin Fansler - [kfansler](https://github.com/kfansler)
- Nathan Armstrong - [armstnp](https://github.com/armstnp)
