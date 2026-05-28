---
name: review-api-endpoint
description: Use when reviewing PRs that add or modify API endpoints - verifying implementation completeness, test coverage, assertion patterns, and documentation updates
---

# Review API Endpoint

## Overview

Systematic checklist for reviewing SDK endpoint implementations. Ensures all 4 required components exist: implementation, tests (5 types with correct assertions), WireMock mappings, and documentation. **Critical: Verify implementation matches OpenAPI spec exactly.**

## When to Use

- Reviewing PR that adds new SDK endpoint
- Reviewing PR that modifies existing endpoint
- Code review for API integration work
- Verifying endpoint implementation follows SDK standards

**GOLD STANDARD VERIFICATION: Compare implementation against tests/mock_api/reports/ during review. Tests should match these patterns exactly.**

**Required before review:** 
1. OpenAPI spec (Smartsheet public API: https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json OR user-provided spec path)
2. WireMock mappings (Smartsheet SDK tests repo: https://github.com/smartsheet/smartsheet-sdk-tests OR user-provided local path)

**Cannot approve without spec AND mappings verification.**

## Review Checklist

Work through each section systematically:

### 0. OpenAPI Spec Verification (MUST BE FIRST)

**Required:** OpenAPI spec URL or path

- [ ] **Obtain spec:** Smartsheet public API (https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json) OR user-provided
- [ ] **If spec not provided:** Request from user - cannot proceed without it
- [ ] Endpoint exists in spec at correct path
- [ ] HTTP method matches spec
- [ ] All parameters match spec (names, types, required/optional)
- [ ] Parameter types match spec (string, integer, boolean, etc.)
- [ ] Request body schema matches spec (for POST/PUT/PATCH)
- [ ] Response schema matches spec (all properties, correct types)
- [ ] Query parameters match spec exactly
- [ ] Path parameters match spec
- [ ] camelCase conversion correct (spec uses camelCase, SDK uses snake_case)

**If any spec mismatch found:** Request changes immediately - do not continue review until fixed.

### 0b. WireMock Mappings Verification (MUST BE SECOND)

**Required:** WireMock mappings location (GitHub repo or local path)

- [ ] **Obtain mappings:** Smartsheet SDK tests (https://github.com/smartsheet/smartsheet-sdk-tests) OR user-provided path
- [ ] **If mappings not provided:** Request from user - cannot proceed without them
- [ ] Verify mapping exists: `/{resource}/{method}/all-response-body-properties`
- [ ] Verify mapping exists: `/{resource}/{method}/required-response-body-properties` (if applicable)
- [ ] Verify global error mappings: `/errors/400-response`, `/errors/500-response`
- [ ] Response jsonBody in mappings matches OpenAPI spec schema
- [ ] Request body in mappings matches OpenAPI spec (for POST/PUT/PATCH)
- [ ] Test scenario names in test files match actual mapping paths

**If any mapping missing or spec mismatch found:** Request changes immediately - do not continue review.

### 0c. Breaking Change Detection (CRITICAL - MUST BE THIRD)

**CRITICAL IMPORTANCE:** Breaking changes in the public SDK contract break user code in production. This check is MANDATORY and NON-NEGOTIABLE.

**Rule:** Unless the PR author EXPLICITLY states "This PR contains breaking changes" with justification, ANY breaking change MUST be flagged and PR MUST be rejected.

**What constitutes a breaking change:**

**Method Signature Changes (BREAKING):**
- [ ] **Removed parameter** - Even if optional, removing breaks users calling with that parameter
- [ ] **Changed parameter from optional to required** - Breaks existing calls without that parameter
- [ ] **Changed parameter type** - `str` → `int`, `List[str]` → `str`, etc.
- [ ] **Changed parameter name** - `sheet_id` → `sheetId` breaks keyword argument calls
- [ ] **Reordered parameters** - Breaks positional argument calls
- [ ] **Removed method** - Breaks all users calling that method

**Return Type Changes (BREAKING):**
- [ ] **Changed return type** - `Sheet` → `List[Sheet]`, `Union[Sheet, Error]` → `Sheet`
- [ ] **Removed `Error` from union** - Breaks `isinstance(response, Error)` checks
- [ ] **Changed response property types** - `id: int` → `id: str` in response model
- [ ] **Removed response properties** - Even if optional, breaks users accessing that property

**Behavior Changes (BREAKING):**
- [ ] **Changed error handling** - Exceptions instead of Error returns, different exception types
- [ ] **Changed side effects** - Method now creates/deletes resources it didn't before
- [ ] **Changed validation rules** - Now rejects previously valid input

**Non-Breaking Changes (ALLOWED):**
- [ ] **Added optional parameter with default** - `def method(x, new_param=None)` is safe
- [ ] **Added new method** - Doesn't affect existing methods
- [ ] **Added optional response properties** - Doesn't break existing property access
- [ ] **Made parameter more permissive** - Required → optional, stricter type → looser type
- [ ] **Expanded accepted input** - Now accepts additional valid values

**Review Process:**

1. **Check PR description first:**
   - Does it say "This PR contains breaking changes" OR "Breaking change:" OR "BREAKING:"?
   - If YES: Verify justification is provided (major version bump, deprecation path, migration guide)
   - If NO: Proceed to step 2

2. **Compare old vs new signatures:**
   - Request git diff showing before/after method signatures
   - Check EVERY change against breaking change list above
   - Even ONE breaking change without explicit documentation = REQUEST CHANGES

3. **If breaking change found without documentation:**
   - **IMMEDIATELY REQUEST CHANGES** - do not proceed with rest of review
   - State: "This PR introduces breaking changes without explicit documentation"
   - List each breaking change specifically
   - Require either:
     - Revert to backward-compatible design, OR
     - Update PR description with "BREAKING CHANGE:" and full justification

4. **If breaking change is documented:**
   - Verify justification is reasonable (not just "cleaner API")
   - Verify migration path is documented
   - Verify version bump strategy is mentioned (major version)
   - If missing any of these: REQUEST CHANGES

**Example Breaking Changes to Flag:**

```python
# BREAKING: Removed parameter
# Before
def get_sheet(self, sheet_id: int, include: List[str] = None)
# After  
def get_sheet(self, sheet_id: int)

# BREAKING: Changed optional to required
# Before
def get_sheet(self, sheet_id: int, format: str = "json")
# After
def get_sheet(self, sheet_id: int, format: str)

# BREAKING: Changed return type
# Before
def get_sheet(self, sheet_id: int) -> Union[Sheet, Error]
# After
def get_sheet(self, sheet_id: int) -> Sheet

# BREAKING: Removed property from response model
# Before: Sheet has .permalink property
# After: Sheet doesn't have .permalink property
```

**Common Rationalizations to REJECT:**

| Excuse | Reality | Response |
|--------|---------|----------|
| "Users probably aren't using that parameter" | You don't know that | REQUEST CHANGES |
| "It's a minor change" | Minor to you ≠ minor to users | REQUEST CHANGES |
| "Tests pass" | Tests don't catch breaking changes to public API | REQUEST CHANGES |
| "OpenAPI spec changed" | SDK still breaks existing user code | REQUEST CHANGES (requires explicit BREAKING CHANGE note) |
| "Better API design" | Breaking user code is not better | REQUEST CHANGES or deprecation path required |
| "Will document in CHANGELOG" | PR description must state it FIRST | REQUEST CHANGES until PR description updated |

**Red Flags - Breaking Change Not Documented:**

These thoughts mean STOP and REQUEST CHANGES immediately:
- "The change makes sense" - Doesn't matter if it breaks users
- "Spec says it's required now" - Still breaks existing SDK users
- "Only affects edge cases" - Still a breaking change
- "Can be fixed in user code easily" - Still requires every user to update
- "Implementation is cleaner" - Not worth breaking users

**The Rule (Repeat for Emphasis):**

**NO BREAKING CHANGES WITHOUT EXPLICIT PR DESCRIPTION STATING "BREAKING CHANGE:" + JUSTIFICATION**

If you find a breaking change and PR description doesn't explicitly mention it: **IMMEDIATE REQUEST CHANGES. DO NOT PROCEED WITH REVIEW.**

### 1. Implementation Quality

**File:** `smartsheet/{resource}.py`

- [ ] **Type definitions exist** for new endpoints (check smartsheet/models/)
- [ ] **Python 3.7 compatibility** - no 3.8+ features (walrus operator :=, positional-only params /, TypedDict, Literal)
- [ ] **Type definitions use Python 3.7 syntax** (from __future__ import annotations if needed)
- [ ] Method signature has proper type hints
- [ ] Docstring with Args and Returns sections
- [ ] Uses SDK patterns: `fresh_operation()` → `prepare_request()` → `request()`
- [ ] HTTP method correct for operation (GET/POST/PUT/DELETE/PATCH)
- [ ] Path uses placeholders: `/resource/{id}` not `/resource/123`
- [ ] Query params conditionally added (only if not None)
- [ ] Request body serialization correct (for POST/PUT/PATCH)
- [ ] Expected type matches actual response structure
- [ ] Return type: `Union[ExpectedType, Error]`

**Reference:** @ADVANCED.md "Resource Module Organization"

### 2. Test Coverage (5 Required Types)

**File:** `tests/mock_api/{resource}/test_{method_name}.py`

**CRITICAL: All 5 test types MUST exist. Tests MUST strictly follow @TESTING.md standards. Check test file has all 5 functions.**

**GOLD STANDARD COMPARISON: Open tests/mock_api/reports/test_create_report.py (or any report test) side-by-side. Implementation should match these patterns exactly - same assertion style, same structure, same helper usage.**

**Test data must match OpenAPI spec:**
- Request test data uses types/formats from spec
- Response assertions match spec schema
- Error tests match spec error responses

- [ ] **`test_{method}_generated_url_is_correct`** exists
  - Uses `get_wiremock_request(request_id)` to retrieve request
  - Parses URL with `urlparse()` and `parse_qs()`
  - **Whole-object query assertion:** `assert query == {...}` (NOT property-by-property)
  - **ALWAYS asserts query parameters, even if empty:** `assert not query`
  - Path assertion matches expected pattern

- [ ] **`test_{method}_all_response_properties`** exists
  - Type safety: `isinstance(response, ExpectedType)`
  - For wrapped responses: checks BOTH `isinstance(response, Result)` AND `isinstance(response.result[0], InnerType)`
  - **Whole-object response assertion:** `assert response.to_dict() == {...}` (NOT properties)
  - **Response structure matches OpenAPI spec schema exactly**
  - Includes request body assertion using `json.loads(wiremock_request["body"])`
  - **Whole-object request assertion:** `assert request_body == {...}`
  - **ALWAYS asserts request body, even if empty for GET/DELETE:** `assert not request_body`
  - For POST/PUT/PATCH: **Request body matches OpenAPI spec schema (camelCase, correct types)**

- [ ] **`test_{method}_required_response_properties`** exists (if applicable)
  - Same assertion patterns as all_response_properties
  - Only required if WireMock mapping exists for minimal response
  - Tests SDK handles responses with only required fields
  - **ALWAYS asserts request body, even if empty for GET/DELETE:** `assert not request_body`

- [ ] **`test_{method}_error_4xx`** exists
  - Uses `/errors/400-response` test scenario
  - Asserts `isinstance(response, Error)`

- [ ] **`test_{method}_error_5xx`** exists
  - Uses `/errors/500-response` test scenario
  - Asserts `isinstance(response, Error)`

**Reference:** 
- @TESTING.md "Mock API Test Standards" (especially lines 136-141 for request body requirements)
- **GOLD STANDARD: tests/mock_api/reports/ - compare PR tests against these patterns**

### 3. Test Quality Issues

Common anti-patterns to catch:

- [ ] **No property-by-property assertions**
  - ❌ Bad: `assert response.id == 123; assert response.name == "test"`
  - ✅ Good: `assert response.to_dict() == {"id": 123, "name": "test"}`

- [ ] **No property-by-property query assertions**
  - ❌ Bad: `assert query["page"] == ["1"]; assert query["pageSize"] == ["100"]`
  - ✅ Good: `assert query == {"page": ["1"], "pageSize": ["100"]}`

- [ ] **Request body assertions for POST/PUT/PATCH**
  - Must exist in `all_response_properties` test
  - Must use `get_wiremock_request(request_id)` and `json.loads()`
  - Must assert complete request body as whole object

- [ ] **Type safety for wrapped responses**
  - Must check wrapper type: `isinstance(response, Result)`
  - Must check inner type: `isinstance(response.result[0], Model)`
  - Not just one or the other - BOTH required

### 4. WireMock Mappings

**Repository:** [smartsheet-sdk-tests](https://github.com/smartsheet/smartsheet-sdk-tests)

**Note:** Cannot directly verify without checking external repo, but look for test scenario names:

- [ ] Test uses scenario: `/{resource}/{method}/all-response-body-properties`
- [ ] Test uses scenario: `/{resource}/{method}/required-response-body-properties` (if applicable)
- [ ] Error tests use: `/errors/400-response` and `/errors/500-response`

**If tests reference non-standard scenarios, flag for WireMock mapping verification.**

### 5. Documentation Updates

**File:** `docs-source/smartsheet_api.rst` (or appropriate .rst file)

- [ ] **Verified docs-source update required per @ADVANCED.md** (not all endpoints need docs updates)
- [ ] If required: Method added to module section with `.. automethod:: {Class}.{method}`
- [ ] Docstring complete (will be rendered by Sphinx)
- [ ] Ask: Has Sphinx build been tested? (`uv run sphinx-build -b html docs-source docs-source/_build/html`)

**Reference:** @CONTRIBUTING.md "Documentation" section and @ADVANCED.md for documentation requirements

### 6. Supporting Files

- [ ] Constants file updated: `tests/mock_api/{resource}/common_test_constants.py`
- [ ] Test IDs, expected values defined as constants
- [ ] No magic numbers in test files

## Quick Reference: Test Count by Endpoint Type

| Endpoint Type | Required Tests | Request Body Assertions |
|---------------|----------------|------------------------|
| GET single | 4-5 (skip required if N/A) | No |
| GET list | 4-5 | No |
| POST | 5 | **Yes** - required |
| PUT | 5 | **Yes** - required |
| PATCH | 5 | **Yes** - required |
| DELETE | 5 | No |

## Review Outcome Decision

**Approve (Ready to Merge):**
- **OpenAPI spec verified and implementation matches exactly**
- **WireMock mappings verified**
- **Tests match gold standard patterns in tests/mock_api/reports/**
- All 5 test types exist (or 4 if required_properties N/A)
- All assertions use whole-object pattern
- Tests strictly follow @TESTING.md standards - **MANDATORY, no exceptions**
- POST/PUT/PATCH include request body assertions
- Type safety checks present (isinstance for wrapper AND inner)
- Documentation updated
- No anti-patterns detected

**Request Changes (MUST block merge - non-negotiable):**
- **No OpenAPI spec provided or not verified**
- **No WireMock mappings provided or not verified**
- **BREAKING CHANGE without explicit PR documentation** (CRITICAL - see Breaking Change Detection section)
- **Missing type definitions for new endpoint**
- **Python 3.8+ features used (must be 3.7 compatible)**
- **Implementation doesn't match spec (parameters, types, structure)**
- **Response/request schemas don't match spec**
- **Tests don't match gold standard patterns**
- Missing any required test type
- Tests don't follow @TESTING.md standards
- Property-by-property assertions present
- Missing request body assertions (POST/PUT/PATCH)
- Incomplete type safety checks
- Documentation missing or incorrect
- WireMock scenario names suggest missing mappings

**Comment/Question:**
- Cannot verify WireMock mappings exist (external repo)
- Sphinx build not confirmed
- Minor style issues (but don't block if spec verified and tests complete)

## Red Flags - Don't Approve Yet

These thoughts mean STOP - review is incomplete:

- **"I don't need to check the spec"** - Spec verification is MANDATORY
- **"I don't need to check WireMock mappings"** - Mappings verification is MANDATORY
- **"I don't need to check for breaking changes"** - Breaking change check is MANDATORY
- **"Change looks reasonable so it's not breaking"** - Must explicitly verify against breaking change list
- **"PR doesn't mention breaking changes so there aren't any"** - You must verify, not trust
- **"Users probably aren't affected"** - Any breaking change requires explicit documentation
- **"It's just following the spec"** - Spec changes can still break SDK users
- **"I didn't compare to reports tests"** - Gold standard comparison is MANDATORY
- **"Tests look similar to reports"** - Must match EXACTLY, not just similar
- **"Implementation looks right"** - Must verify against spec, not intuition
- **"Spec roughly matches"** - Must match EXACTLY, not roughly
- **"Mappings probably exist"** - Must verify, not assume
- "Tests pass, looks good" - Check assertion patterns, not just pass/fail
- "Has error tests" - Verify BOTH 4xx and 5xx exist
- "All 5 tests present" - Check quality, not just count
- "Implementation works" - Tests and docs still required
- "Minor change" - Still needs complete test coverage and spec verification
- Saw property-by-property assertions but didn't flag them
- POST/PUT/PATCH tests exist but didn't check for request body assertions
- Only checked one type in isinstance() for wrapped responses
- Tests don't strictly follow @TESTING.md but "close enough"
- "Type definitions are optional" - Required for new endpoints
- "Python 3.9 syntax is fine" - Must be 3.7 compatible
- Didn't verify ADVANCED.md docs requirements

**All of these mean: Review incomplete. Verify spec and mappings first, compare to gold standard, then work through checklist systematically.**

## Common Review Mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| Didn't check OpenAPI spec | Cannot verify correctness without it | Get spec, verify every detail |
| Didn't check for breaking changes | Breaking changes break user code | Compare old/new signatures explicitly |
| "No breaking changes mentioned" | You must verify, not trust | Check every signature change against breaking change list |
| "Change seems reasonable" | Reasonable ≠ non-breaking | Verify against explicit breaking change criteria |
| "Spec roughly matches" | Must match EXACTLY | Compare every parameter/field |
| "Tests pass, looks good" | Passing ≠ complete coverage | Check all 5 types exist |
| "Has error tests" | Only checking 1 of 2 error types | Both 4xx AND 5xx required |
| "Response assertions look fine" | Property-by-property missed | Must use `.to_dict() == {...}` |
| "POST test complete" | Missing request body assertion | Check TESTING.md line 136-141 |
| "Type checking present" | Only wrapper or only inner | Must check BOTH types |
| Missing query assertion pattern | Allows unexpected params | Must assert complete query object |
| "Docs aren't critical" | Sphinx won't discover method | Documentation required, not optional |
| Approving under time pressure | Quality > speed | Request changes, cite standards |
| "Tests look good enough" | Must strictly follow TESTING.md | Reference @TESTING.md standards |
| Didn't verify WireMock mappings | Tests may reference non-existent mappings | Check repo or local path |
| "Mappings probably exist" | Cannot assume - must verify | Verify actual mapping files exist |
| "Type hints are optional" | Type definitions MANDATORY for new endpoints | Request type defs |
| Didn't check Python version | Must support 3.7, no 3.8+ | Verify compatibility |
| Assumed docs needed | Check ADVANCED.md requirements | Verify docs actually needed |

## Example Review Comments

**For missing OpenAPI spec:**
```
Cannot proceed with review. OpenAPI spec required for verification.

Please provide:
- Smartsheet public API spec: https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json
- OR path to custom OpenAPI spec for this endpoint

Will verify implementation matches spec exactly before approving.
```

**For breaking changes without documentation:**
```
CRITICAL: This PR introduces breaking changes without explicit documentation.

Breaking changes found:
1. Removed optional parameter `include` - breaks calls using this parameter
2. Changed return type from `Union[Sheet, Error]` to `Sheet` - breaks error handling code
3. Changed parameter `format` from optional to required - breaks calls without this parameter

**Impact:** These changes will break existing user code in production.

**Required actions:**
- Either: Revert to backward-compatible design (keep optional params, maintain Union return type)
- Or: Update PR description with "BREAKING CHANGE:" header and provide:
  - Justification for breaking changes
  - Migration path for existing users
  - Version bump strategy (major version)

Cannot approve until breaking changes are either removed or explicitly documented with justification.
```

**For spec mismatch:**
```
Request changes: Implementation doesn't match OpenAPI spec.

Issues found:
- Parameter `pageSize` type: spec says integer, implementation uses string
- Missing required parameter `objectType` from spec
- Response field `directId` not in spec schema
- Query parameter `includeAll` in implementation but not in spec

Please update implementation to match spec exactly at:
[spec path/section]
```

**For missing test types:**
```
Not ready to merge. Missing 3 of 5 required test types:
- test_{method}_required_response_properties (if applicable)
- test_{method}_error_4xx  
- test_{method}_error_5xx

See TESTING.md "Mock API Test Standards" for complete requirements.
```

**For property-by-property assertions:**
```
Test assertion pattern needs fixing:

Current (line X):
assert response.id == 123
assert response.name == "test"

Required pattern (TESTING.md):
assert response.to_dict() == {
    "id": 123,
    "name": "test"
}

Whole-object assertions prevent unexpected properties from creeping in.
```

**For missing request body assertions (POST/PUT/PATCH):**
```
POST/PUT/PATCH endpoints require request body assertions (TESTING.md lines 136-141).

Add to test_{method}_all_response_properties:

wiremock_request = get_wiremock_request(request_id)
request_body = json.loads(wiremock_request["body"])
assert request_body == {
    # expected request structure
}

This verifies serialization correctness (camelCase conversion, etc).
```

**For missing type definitions:**
```
Request changes: Missing type definitions for new endpoint.

New endpoints require type definitions in smartsheet/models/.

Required types:
- Request model (if POST/PUT/PATCH with body)
- Response model matching OpenAPI spec schema

All types must be Python 3.7 compatible (no 3.8+ syntax).

See existing models in smartsheet/models/ for patterns.
```

**For Python 3.8+ compatibility issues:**
```
Request changes: Code uses Python 3.8+ features.

This SDK must support Python 3.7. Found:
- Line X: Walrus operator := (requires 3.8)
- Line Y: positional-only parameter / (requires 3.8)
- Line Z: TypedDict without typing_extensions (requires 3.8)

Please update to Python 3.7 compatible syntax.
```

**For tests not matching gold standard:**
```
Tests don't match gold standard patterns. Please review tests/mock_api/reports/ and update:

Current issues:
- Property-by-property assertions (should be `.to_dict() ==`)
- Missing complete query parameter assertion
- Error tests don't follow reports pattern
- Missing request body assertions for POST

Compare your test structure against:
- tests/mock_api/reports/test_create_report.py (POST example)
- tests/mock_api/reports/test_add_report_columns.py (POST example)

Tests should match these patterns exactly.
```

## The Bottom Line

**Review is about spec compliance, gold standard pattern matching, and completeness verification.**

Implementation can work perfectly but:
- Not match OpenAPI spec (wrong types, missing parameters, extra fields)
- Not match gold standard patterns in tests/mock_api/reports/
- Be incomplete (no tests, no docs)
- Have tests that pass but use wrong assertion patterns
- Have tests that don't follow @TESTING.md standards
- Have documentation that exists but doesn't build

**Review workflow:**
1. **Verify OpenAPI spec first** - cannot proceed without this
2. **Verify WireMock mappings** - cannot proceed without these
3. **Open tests/mock_api/reports/ for side-by-side comparison**
4. Check implementation matches spec exactly
5. **Verify tests match gold standard patterns exactly**
6. Verify all 5 test types exist and follow @TESTING.md strictly
7. Check assertion patterns (whole-object, not property-by-property)
8. Verify documentation updates

Approve only when spec verified AND mappings verified AND patterns match gold standard AND all 4 components are complete and correct.
1. **Verify OpenAPI spec first** - cannot proceed without this
2. Check implementation matches spec exactly
3. Verify all 5 test types exist and follow @TESTING.md strictly
4. Check assertion patterns (whole-object, not property-by-property)
5. Verify documentation updates

Approve only when spec verified AND all 4 components are complete and correct.
