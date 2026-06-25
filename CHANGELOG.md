# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [x.x.x] - Unreleased

### Fixed

- Added missing `SHARED` value to `PublishAccessibleBy` enum.

### Added

- Added support for GET /2.0/sheets/{sheetId}/path endpoint (`get_sheet_path`)
- Added support for GET /2.0/reports/{reportId}/path endpoint (`get_report_path`)
- Added support for GET /2.0/sights/{sightId}/path endpoint (`get_sight_path`)
- Added support for GET /2.0/folders/{folderId}/path endpoint (`get_folder_path`)
- Added helper methods `get_leaf_<asset>()` and `get_leaf_<asset>_path()` to the responses of the path endpoints for convenient traversal

## [4.0.2] - 2026-06-10

### Fixed

- Deprecation related corrections

### Added

- Hardcode `paginationType=token` for `list_workspaces`.

## [4.0.1] - 2026-06-09

### Fixed

- Packaging bug after migrating to uv. [#144](https://github.com/smartsheet/smartsheet-python-sdk/issues/144)

## [4.0.0] - 2026-06-08

### Added

- Added `object_id_str` field to `Event` model to support alphanumeric object identifiers (AUD-902)
- SDK architecte details in [ADVANCED.md](ADVANCED.md)
- SDK testing standards in [TESTING.md](TESTING.md)

### Removed

- ⚠️ **BREAKING**: Removed deprecated `include_all` parameter from `list_webhooks`. This was [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04) (sunset Jun-03-2026). Use offset-based pagination via `page` and `page_size` (server-capped at 10,000).
- ⚠️ **BREAKING**: Removed deprecated `include_all`, `page`, `page_size`, `modified_since`, and `pagination_type` parameters from `list_sights`. These were [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#deprecated-includeall-and-offset-based-pagination-for-dashboards) (sunset Jun-03-2026). `list_sights` now uses token-based pagination exclusively and returns `TokenPaginatedResult[Sight]`. Use `max_items` and `last_key` instead.
- ⚠️ **BREAKING**: Removed deprecated `include_all`, `page`, `page_size`, and `pagination_type` parameters from `list_workspaces`. These were [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04) (sunset Jun-03-2026). `list_workspaces` now uses token-based pagination exclusively and returns `TokenPaginatedResult[Workspace]`. The response no longer exposes `page_number`, `page_size`, `total_count`, or `total_pages`. Use `max_items` and `last_key` instead. The new shape mirrors `list_sights`.
- ⚠️ **BREAKING**: Removed `list_public_templates` and `list_user_created_templates` from the `Templates` class. The `Templates` class and `Smartsheet.Templates` accessor have been removed entirely. The underlying `GET /templates` and `GET /templates/public` endpoints were [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04) (sunset Jun-03-2026). Migrate to `get_workspace_children` / `get_folder_children` with `children_resource_types` set to `['sheets', 'templates']` (both values are required — omitting `sheets` will exclude templates from the response) to list templates within a specific workspace or folder.
- ⚠️ **BREAKING**: Removed `get_folder` and `list_folders` from the `Folders` class, and `get_workspace` and `list_folders` from the `Workspaces` class. The underlying `GET /folders/{folderId}`, `GET /folders/{folderId}/folders`, `GET /workspaces/{workspaceId}`, and `GET /workspaces/{workspaceId}/folders` endpoints were [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04) (sunset Jun-03-2026). Migrate to `get_folder_metadata` + `get_folder_children` and `get_workspace_metadata` + `get_workspace_children`. Use `children_resource_types` to filter the children response (e.g., `folders` to replicate the old list-folders behavior).
- ⚠️ **BREAKING**: Removed the deprecated share methods (`share_sheet`/`share_report`/`share_sight`/`share_workspace`, `list_shares`, `get_share`, `update_share`, `delete_share`) from the `Sheets`, `Reports`, `Sights`, and `Workspaces` classes. The underlying asset-specific sharing endpoints were [deprecated by the Smartsheet API](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04) (sunset Jun-03-2026). Migrate to `client.Sharing` (`list_asset_shares`, `get_asset_share`, `share_asset`, `update_asset_share`, `delete_asset_share`), passing `asset_type` and `asset_id`. Note updates now use `PATCH` instead of `PUT`.

### Changed

- `list_webhooks`: server-side behavior changes documented in the docstring. As of the Jun-03-2026 sunset date, `page_size` is server-capped at 10,000, `total_count` and `total_pages` return `-1`, and results are sorted by creation date (most recent first) instead of name. SDK signature unchanged. See [Smartsheet API changelog 2025-08-04](https://developers.smartsheet.com/api/smartsheet/changelog#2025-08-04).

### Fixed

- Aligned the [reports mock api tests](tests/mock_api/reports/) with the testing standards.
- Fixed `access_level` property of [CreateReportResult](smartsheet/models/create_report_result.py) to return `EnumeratedValue` instead of the raw enum itselt.
- Fixed `destination_type` property of [ReportDestination](smartsheet/models/report_destination.py) to return `EnumeratedValue` instead of the raw enum itselt.
- Fixed `asset_type` property of [ReportScopeInclusion](smartsheet/models/report_scope_inclusion.py) to return `EnumeratedValue` instead of the raw enum itselt.
- Fixed `EnumeratedValue.__str__` to return value if the underlying enum inherits from `str`.
- Fixed `serialize` function to use `EnumeratedValue.value.value` if the underlying enum inherits from `str`.

## [3.9.0] - 2026-04-30

### Added

- Support for POST /2.0/reports endpoint
- WireMock integration tests for POST /2.0/reports endpoint including request body serialization validation
- Support for POST /2.0/reports/{reportId}/columns endpoint
- New `add_report_columns()` method in Reports class to add columns to a report
- WireMock integration tests for POST /2.0/reports/{reportId}/columns endpoint
- Support for PUT /2.0/reports/{reportId}/definition endpoint
- New `update_report_definition()` method in Reports class to update report definitions
- WireMock integration tests for report definition update endpoint including nested filter validation
- Support for POST /2.0/reports/{reportId}/scope endpoint
- Support for DELETE /2.0/reports/{reportId}/scope endpoint
- WireMock integration tests for POST /2.0/reports/{reportId}/scope endpoint
- WireMock integration tests for DELETE /2.0/reports/{reportId}/scope endpoint
- Support for DELETE /2.0/reports/{reportId} endpoint
- Add `CONTRIBUTOR` seat type to `SeatType`, `UpgradeSeatType`, and `DowngradeSeatType` enums
- Add mock API tests for `CONTRIBUTOR` seat type in list users and downgrade user operations
- Add `displayContributorSeatType` query parameter to `list_users()` and `list_user_plans()` methods
  - When `true`, VIEWER seat types to CONTRIBUTOR in the response
  - When `false` or omitted, re-writes CONTRIBUTOR seat types to VIEWER in the response

### Fixed

- Fix AttributeError and TypeError exception handling

## [3.8.0] - 2026-04-17

### Added

- Added support for the GET /2.0/favorites/{favoriteType}/{favoriteId} endpoint
- Added directId and name fields to the Favorite model
- Added FavoriteType enum
- WireMock integration tests for contract testing for GET /2.0/favorites/{favoriteType}/{favoriteId} endpoint

## [3.7.2] - 2026-01-29

### Added

- Add `Cells` class to `Smartsheet` class for IDE autocomplete support. Now auto-complete like `smart.Cells.get_cell_history()` and `smart.Cells.add_image_to_cell()` will work.

## [3.7.1] - 2025-12-12

### Fixed

- Update correct method types, which may return either list or a singleton object

## [3.7.0] - 2025-12-11

### Added

- Typing to all SDK service methods

## [3.6.0] - 2025-12-04

### Added

- Support for POST /2.0/users/{userId}/reactivate endpoint
- Support for POST /2.0/users/{userId}/deactivate endpoint

## [3.5.6] - 2025-11-18

### Removed

- Remove integration tests from the sdk test suite

### Added

- Add support for code completion. Now code editors will be able to recognize and complete expressions like `smart.Users` and `smart.Users.list_users`.

### Updated

- Improved the generated reference documentation.
- ADVANCED.md integration and mock api testing documentation

## [3.5.5] - 2025-11-11

### Fixed

- Fix response body logging. When the response Content-Type is application/json the response body is logged.

### Added

- WiremMock integration tests for contract testing for GET /2.0/users/{userId}/plans and GET /2.0/users endpoints
- WireMock integration tests for contract testing for POST /2.0/users/{userId}/plans/{planId}/upgrade and POST /2.0/users/{userId}/plans/{planId}/downgrade
- WireMock integration tests for contract testing for DELETE /{userId}/plans/{planId} endpoint
- Add dict serialization tests
- Add missing properties from [AssetShare](smartsheet/models/asset_share.py): `cc_me`, `message`, `subject`.

### Updated

- Folder structure for the Users related WireMock tests

## [3.5.4] - 2025-10-31

### Fixed

- [Issue-92](https://github.com/smartsheet/smartsheet-python-sdk/issues/92): Only include the `smartsheet` package in the build.

## [3.5.3] - 2025-10-31

### Fixed

- The new sharing endpoints (/2.0/shares) return string for userId and groupId, adjust the SDK to that.

### Added

- `AssetShare` model to fully comply with the new sharing endpoints (/2.0/shares) DTO.

## [3.5.2] - 2025-10-29

### Fixed

- Fix list_asset_shares to return AssetSharesPaginatedResult.
- Fix update_asset_share to return Share

## Added

- Add AssetSharesPaginatedResult for list asset shares.
- Add mock api tests for sharing endpoints.

## [3.5.1] - 2025-10-28

### Fixed

- Rename asset_shares.py to sharing.py so that `Smartsheet.__getattr__` can pick it up.

## [3.5.0] - 2025-10-24

### Added

- Add robust error handling. The SDK won't throw an exception if the error response body is not JSON or properties are missing.
- Add provisionalExpirationDate field to the user_model and user_plan models

## [3.4.0] - 2025-10-20

### Fixed

- Fix minor lint issue
- Use pytest directly to run tests
- Fix @deprecated decorator use.

## [3.3.0] - 2025-10-07

### Added

- Support for new asset-based sharing endpoints in a new `sharing` module:
  - `list_asset_shares`: List all shares for a specified asset
  - `get_asset_share`: Get a specific share for a specified asset
  - `share_asset`: Share an asset with specified users and/or groups
  - `update_share`: Update a specific share for a specified asset
  - `delete_share`: Delete a specific share for a specified asset
- Added `AssetType` enum for use with sharing endpoints

### Updated

- Deprecated old sharing endpoints in the `sheets` module
- Added deprecation notices and migration examples in documentation

## [3.2.0] - 2025-09-25

### Added

- Support for POST /2.0/users/{userId}/plans/{planId}/downgrade
- Support for POST /2.0/users/{userId}/plans/{planId}/upgrade
- Support for GET /2.0/users/{userId}/plans
- Support for GET /2.0/users?planId={planId}&seatType={seatType}
- Support for DELETE /2.0/users/{userId}/plans/{planId}

## [3.1.0] - 2025-08-28

### Added

- New `get_workspace_metadata()` method to get workspace metadata without children
- New `get_workspace_children()` method to get workspace children with filtering and pagination support
- New `get_folder_metadata()` method to get folder metadata without children
- New `get_folder_children()` method to get folder children with filtering and pagination support
- New `TokenPaginatedResult<T>` generic model for type-safe paginated API responses
- New `PaginatedChildrenResult` model with custom deserialization for mixed children types based on resourceType
- Updated `list_workspaces()` method to support Token-based pagination . Use the new `pagination_type='token'` parameter with `last_key` and `max_items` for more efficient pagination. When `pagination_type='token'` is used, the method returns a `Result` object containing `data` and `lastKey`.

### Deprecated

- `get_workspace()` - Use `get_workspace_metadata()` and `get_workspace_children()` instead
- `list_folders()` in Workspaces - Use `get_workspace_children()` with `children_resource_types=['folders']` instead
- `get_folder()` - Use `get_folder_metadata()` and `get_folder_children()` instead
- `list_folders()` in Folders - Use `get_folder_children()` with `children_resource_types=['folders']` instead
- `create_folder()` in Home
- `create_sheet()` in Home
- `create_sheet_from_template()` in Home
- `list_all_contents()` in Home
- `list_folders()` in Home
- `page_size`, `page`, and `include_all` parameters in `list_workspaces()` method are now deprecated. Use `pagination_type='token'` with `max_items` and `last_key` instead. Deprecated parameters will issue `DeprecationWarning` when used.

## [3.0.5] - 2025-04-07

### Changed

- Fallback filename for `DownloadedFile` when `Content-Disposition` header is missing.

## [3.0.4] - 2024-07-29

### Changed

- Changed `serialize` function to also handle dicts - this allows the Event Reporting API to
  return the `additionalDetails` object correctly

### Added

- `to` parameter added for Event Reporting - allows setting an end timestamp for filtering for
  events

## [3.0.3] - 2024-07-17

### Fixed

- fix for [issue 43](https://github.com/smartsheet/smartsheet-python-sdk/issues/43) KeyError: 'content-type'

## [3.0.2] - 2023-05-15

### Updated

- Update urllib3 default retryable methods reference

## [3.0.1] - 2023-03-31

### Updated

- Changing import order to better support later versions of python

## [3.0.0] - 2022-12-06

### Updated

- Migrated SDK to new project

### Added

- Add Github Actions pipeline
- Added linting with Pylint
- Added markdown linting

## [2.177.0] - 2022-08-03

### Added

- add support for commenter permissions
- add base URL for smartsheet.eu
- add `level` parameter to get_row

### Changed

- pull updates for Python 3.10 compatibility
- update setup and readme for Python version 3.7 - 3.10
- update EnumeratedValue `__eq__` method to handle comparisons to NoneType

### Fixed

- separate `DatetimeObjectValue` from `DateObjectValue` to fix Sheet Summary Field serialization

## [2.105.1] - 2020-10-15

### Fixed

- don't add time offset to date types when serializing

## [2.105.0] - 2020-10-07

### Added

- add column formulas
- add filterId to get_sheets
- Adding rowsModifiedSince parameter to sheet.get_sheet
- add `rules` and `ruleRecipients` to create sheet from template
  inclusion

## [2.101.0] - 2020-08-01

### Changed

- #144 bumped missing property message to debug.
- Model Profile Image as different object from Image

### Added

- Webhooks for Columns

## [2.86.0] - 2019-11-12

### Added

- type and object definitions to support multi-picklist columns

### Changed

- additions to CellDataItem widget contents to support METRIC widgets
  containing sheet summary fields
- dashboards widget model to support widgets that are in an error state
- get_columns needs level support
- update doc to indicate format and objectValue are valid for cell
  history includes
- continue to support level 0 widget type names

### Other

- Make INFO+ level logging return either strings or well-formed json for
  log parsing

## [2.83.0] - 2019-08-14

### Added

- add support for sheet summary

## [2.77.0] - 2019-08-08

### Added

- column descriptions
- additional date formats

### Changed

- enable Coveralls
- cleaned up include/exclude flags on copy sheet/folder/workspace
- Significant overhaul of Sights

### Fixed

- Fix logging to use existing module logger instead of a new logger'util'

## [2.68.3] - 2019-06-14

### Changed

- automated doc updates should be ignored in changelist

### Fixed

- bug-21961 sendEmail is hardcoded to true in share_sheet api

### Other

- doc: update CHANGELOG.md
- doc: build 2.68.2 final docs

## [2.68.2] - 2019-06-14

### Changed

- install dependencies for sphinx
- automated doc updates should be ignored in changelist

## [2.68.1] - 2019-06-14

### Fixed

- fix arguments for current versions of pytest

## [2.68.0] - 2019-05-09

### Added

- Event Reporting functionality

## [1.5.0] - 2019-03-19

### Added

- WEBCONTENT sight widget type
- Add Workspace to sheet model
- Support for groups in get_current_user
- Multi-contact feature support

### Fixed

- Fixed setter for modified_at attribute in row model

## [1.4.0] - 2019-02-19

### Added

- Added BASE URI definition for Smartsheetgov

### Changed

- Remove [enum34](https://pypi.python.org/pypi/enum34) as a dependency for versions of Python after 3.4

## [1.3.3] - 2018-04-19

### Added

- XLSX and CSV import endpoints for workspaces, folders and sheets
- Rudimentary support Sight chart objects (chart contents read into JSON strings)
- Exclude `permalinks` option to Home.list_all_contents
- backgroundColor to Sight object

### Fixed

- [Improper format strings in Types](https://github.com/smartsheet-platform/smartsheet-python-sdk/issues/92)

## [1.3.2] - 2018-03-15

### Fixed

- String representations for EnumeratedValue should contain just their `name` not `class_name.name`
[(SO reported)](https://stackoverflow.com/questions/49256434/writing-column-type-now-has-columntype-option-instead-of-option).

## [1.3.1] - 2018-03-01

### Added

- Implemented [cross-sheet References](http://smartsheet-platform.github.io/api-docs/?shell#cross-sheet-references)
- Updated UserProfile and added support for profile images
- Added an argument to the client constructor method to externally set the API base URI
- Implemented [Automation Rules](http://smartsheet-platform.github.io/api-docs/?shell#automation-rules)
- Implemented row sort objects and [Sort Rows in Sheet](http://smartsheet-platform.github.io/api-docs/?shell#sort-rows-in-sheet) endpoint
- Added row filter properties to SheetFilter
- Added ifVersionAfter parameter to Sheet.get_sheet() method

### Changed

In our efforts to further streamline the SDK, enumerated properties have been changed from type String to type EnumeratedValue, which wraps Python Enum.
In addition to allowing us to remove a number of redundant string arrays, this also provides the benefit of better code completion (in most IDEs)
and provides for more programmatic clarity, for example:

 ```python
sheet = smartsheet.Sheets.get_sheet(sheet_id)
if sheet.access_level == AccessLevel.OWNER:
    # perform some task for OWNER
    ...
```

However, string comparisons will continue to operate as they did previously. No change is required if your code uses comparisons such as:

```python
sheet = smartsheet.Sheets.get_sheet(sheet_id)
if sheet.access_level == 'OWNER':
    # perform some task for OWNER
    ...
```

[enum34](https://pypi.python.org/pypi/enum34) has been added as a required package for the SDK

## [1.3.0] - 2018-02-21

### Changed

Several changes have been made to the SDK to improve both the maintainability of the SDK and the predictability/reliability of the results returned by the SDK. Some of these changes may be breaking to code that currently uses the SDK. The following changes should be reviewed:

- The JSON serializer has been changed to ignore `null` values and empty lists (`[]`). A new Smartsheet model, ExplicitNull, is provided for circumstances where there is a need to force the serialization of a null value. As an example, to clear a hyperlink value from a cell, you can perform the following operation:

```python
        first_row = Row()
        first_row.id = 10
        first_row.cells.append({
            "columnId": 101,
            "value": "",
            "hyperlink": ExplicitNull()
        })

        response = self.client.Sheets.update_rows(1, [first_row])
```

- Property values are more strongly type checked on assignment and you will get a `ValueError` exception if you attempt to assign an incompatible object. Previously, there were a number of cases where assignment of incompatible types would have resulted in a silent failure by the SDK.
- In previous releases, property filters were executed prior to create or update operations on many models within the SDK. Unfortunately, those filters were sometimes at odds with the API and occasionally returned unpredictable results. For that reason those filters have been removed. Be aware that any property that is set in a model will be passed through to the API.
- Properties `id`, `format`, and `type` are accessible without the preceding underscore, e.g. `cell._format` has changed to `cell.format`.

## [1.2.4] - 2018-02-21

### Fixed

- There is a race condition which exists in the window between when the API servers disconnect an idle connection and when the client receives notification
of the disconnection. If a request is made during that window, the client reads a blank status line and issues an error indicating that the session was
terminated without a response (UnexpectedRequestError). This release is made to address that issue by implementing appropriate retries in the SDK.

## [1.2.3] - 2017-12-11

### Fixed

- Safe defaults for mock api test name and module name

## [1.2.2] - 2017-12-07

### Added

- Support for column validation
- New `Passthrough` object supports `get`, `post`, `put`, or `delete` with arbitrary json payload. Use this for access to any API feature that isn't yet modeled in the API. Requests still benefit from error retry and logging.

- `add_image_to_cell` & `attach_file_to_cell`: Now support `override_validation` and `alt_text` parameters
- `copy_folder`, `copy_workspace` and `copy_sheet`: Additional options for `include`, `skip_remap`, and `omit` parameters
- Support for `include=sheetVersion` for several endpoints that return a list of sheets
- Support for reading sheet filters
- More flags when publishing Sheets or Reports as HTML
- Search
  - Results include favorite information
  - Limit search scope

### Changed

- Mock tests
- Improved logging

### Fixed

- Sight widget column property name

## Previous releases

- Documented as [Github releases](https://github.com/smartsheet-platform/smartsheet-python-sdk/releases)
