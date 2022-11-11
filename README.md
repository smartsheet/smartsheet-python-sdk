# Smartsheet Python SDK
![Build Status](https://github.com/smartsheet/smartsheet-python-sdk/actions/workflows/publish-distribution.yaml/badge.svg) [![Coverage Status](https://coveralls.io/repos/smartsheet-platform/smartsheet-python-sdk/badge.svg?branch=master&service=github)](https://coveralls.io/github/smartsheet-platform/smartsheet-python-sdk?branch=master) [![PyPI version](https://badge.fury.io/py/smartsheet-python-sdk.svg)](https://badge.fury.io/py/smartsheet-python-sdk)

A library for connecting to the [Smartsheet API](https://smartsheet.redoc.ly) from Python applications.

## Requirements
The SDK is compatible with [actively supported](https://devguide.python.org/versions/#versions) Python versions `3.10`, `3.9`, `3.8`, `3.7`.

## Installation

To install using [pip](http://www.pip-installer.org/):

```bash
pip install smartsheet-python-sdk
```
## Getting Started
To get started with the Smartsheet Python SDK:

1.  Set **SMARTSHEET_ACCESS_TOKEN** in your environment, using your Smartsheet API key. Find out more about [Authentication and Access Tokens](https://smartsheet.redoc.ly/#section/API-Basics/Authentication-and-Access-Tokens) in the Smartsheet API Documentation. You can generate an access token in Smartsheet UI under Account > Personal Settings > API Access.

2.  Install the Smartsheet Python SDK (see [installation instructions](###installation) above)

3.  The following snippet shows how to create a Smartsheet client and perform some basic actions using the SDK. Ensure your Smartsheet user has access to at least one sheet.
```python
import smartsheet

smart = smartsheet.Smartsheet()             # Create a Smartsheet client 

response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
sheetId = response.data[0].id               # Get the ID of the first sheet in the response
sheet = smart.Sheets.get_sheet(sheetId)     # Load the sheet by using it's ID

print(f"The sheet {sheet.name} has {sheet.total_row_count} rows")   # Print some information about the sheet
```
## Documentation
Use the following resources to learn more about the SDK capabilities:
1. [Smartsheet Python SDK sample project](https://github.com/smartsheet-samples/python-read-write-sheet)
2. [Python SDK documentation](https://smartsheet.github.io/smartsheet-python-sdk/)
3. [Smartsheet API Documentation](https://smartsheet.redoc.ly)

## Advanced Topics
For details about logging, testing, how to use a passthrough option, and how to override HTTP client behavior, 
see [Advanced Topics](ADVANCED.md).

## Contributing
If you would like to contribute a change to the SDK, please fork a branch and then submit a pull request. See the [Contributing.md](contributing.md) for more details

## Acknowledgements
