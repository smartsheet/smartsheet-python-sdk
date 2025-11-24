.. toctree::
    :maxdepth: 2
    :hidden:

    smartsheet_api
    smartsheet_models
    smartsheet_enums
    smartsheet_types
    smartsheet_exceptions

Smartsheet Python SDK Documentation
===================================

* Release v\ |version|

* `GitHub repository <https://github.com/smartsheet/smartsheet-python-sdk>`_

* `Changelog <https://github.com/smartsheet/smartsheet-python-sdk/blob/mainline/CHANGELOG.md>`_

Installation
------------

To install using pip::

    pip install smartsheet-python-sdk

Quickstart
----------

Getting started is easy:

#.  Get your Smartsheet API access token. Find out more about getting
    `direct API access <https://developers.smartsheet.com/api/smartsheet/guides/getting-started>`_ in the Smartsheet API Documentation.
    You can generate an access token in Smartsheet UI under Account > Personal Settings > API Access.

#.  Install the Smartsheet Python SDK from the `Python Package Index <http://pypi.python.org/pypi/smartsheet-python-sdk>`_,
    or by using "pip install smartsheet-python-sdk".

#.  Import the smartsheet module and start using the SDK (see examples below).

Authentication
--------------

You can authenticate with the Smartsheet API in two ways:

**Option 1: Environment Variable (Recommended)**

Set the **SMARTSHEET_ACCESS_TOKEN** environment variable::

    export SMARTSHEET_ACCESS_TOKEN="your_token_here"

Then create the client without parameters::

    import smartsheet
    smart = smartsheet.Smartsheet()

**Option 2: Direct Token**

Pass the access token directly to the Smartsheet constructor::

    import smartsheet
    smart = smartsheet.Smartsheet(access_token='your_token_here')

Example Usage
-------------

Basic Example
~~~~~~~~~~~~~

The following example shows how to create a Smartsheet client and perform some basic operations::

    import smartsheet

    # Create a Smartsheet client (uses SMARTSHEET_ACCESS_TOKEN environment variable)
    smart = smartsheet.Smartsheet()

    # Or create with explicit token:
    # smart = smartsheet.Smartsheet(access_token='your_token_here')

    # List all sheets
    response = smart.Sheets.list_sheets()

    # Get the ID of the first sheet
    sheet_id = response.data[0].id

    # Load the sheet by using its ID
    sheet = smart.Sheets.get_sheet(sheet_id)

    # Print information about the sheet
    print(f"The sheet {sheet.name} has {sheet.total_row_count} rows")

Working with Rows
~~~~~~~~~~~~~~~~~

Add rows to a sheet::

    import smartsheet

    smart = smartsheet.Smartsheet()

    # Build new row
    new_row = smart.models.Row()
    new_row.to_top = True
    new_row.cells.append({
        'column_id': 123456789,
        'value': 'New Value'
    })

    # Add rows to sheet
    response = smart.Sheets.add_rows(sheet_id, [new_row])

Working with Cells
~~~~~~~~~~~~~~~~~~

Update cell values::

    import smartsheet

    smart = smartsheet.Smartsheet()

    # Build new cell value
    new_cell = smart.models.Cell()
    new_cell.column_id = 123456789
    new_cell.value = 'Updated Value'
    new_cell.strict = False

    # Build the row to update
    new_row = smart.models.Row()
    new_row.id = 987654321
    new_row.cells.append(new_cell)

    # Update rows
    response = smart.Sheets.update_rows(sheet_id, [new_row])

Additional Resources
--------------------

For more examples and detailed documentation:

* `Smartsheet Python SDK sample project <https://github.com/smartsheet-samples/python-read-write-sheet>`_
* `Smartsheet API Documentation <https://developers.smartsheet.com/api/smartsheet/introduction>`_ for dozens of Python SDK usage examples
