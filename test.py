import smartsheet

smart = smartsheet.Smartsheet(access_token="7FQvrGGM8gXpDtYnuKpbnDBmFtbOncXyMT38V", api_base="https://api.test.smartsheet.com/2.0")             # Create a Smartsheet client

response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
sheetId = response.data[0].id               # Get the ID of the first sheet in the response
sheet = smart.Sheets.get_sheet(sheetId)     # Load the sheet by using its ID

#print(f"The sheet {sheet.name} has {sheet.total_row_count} rows")   # #Print information about the sheet


def test_row_operations(grid_id, iterations):
    """Test creating, updating, and deleting a row N times on a specific grid."""

    for i in range(iterations):
        #print(f"\nIteration {i + 1}/{iterations}")

        # Get the sheet to find column IDs
        sheet = smart.Sheets.get_sheet(grid_id)
        column_id = sheet.columns[0].id

        # Create a row
        new_row = smartsheet.models.Row()
        new_row.to_bottom = True
        new_row.cells.append({
            'column_id': column_id,
            'value': f'Test Row {i + 1}'
        })

        #print(f"  Creating row...")
        create_response = smart.Sheets.add_rows(grid_id, [new_row])
        row_id = create_response.data[0].id
        #print(f"  Created row with ID: {row_id}")

        # Update the row
        updated_row = smartsheet.models.Row()
        updated_row.id = row_id
        updated_row.cells.append({
            'column_id': column_id,
            'value': f'Updated Test Row {i + 1}'
        })

        #print(f"  Updating row...")
        smart.Sheets.update_rows(grid_id, [updated_row])
        #print(f"  Updated row {row_id}")

        # Delete the row
        #print(f"  Deleting row...")
        smart.Sheets.delete_rows(grid_id, [row_id])
        #print(f"  Deleted row {row_id}")


# Run the test with sheet ID and number of iterations
test_row_operations(sheetId, 250)