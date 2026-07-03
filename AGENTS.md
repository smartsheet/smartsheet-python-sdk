# AI Agent Workflows for Smartsheet Python SDK

This document defines workflow agents for developing the Smartsheet Python SDK. Each agent has a specific role, uses dedicated skills, and follows strict requirements to maintain SDK quality.

## Overview

**Purpose:** Agent-specific guidance for SDK API endpoint development

**Relationship to other documentation:**

- **CLAUDE.md**: Provides SDK-specific development context and patterns
- **Skills** (`.claude/skills/`): Contain detailed execution checklists
- **Supporting docs**: TESTING.md, ADVANCED.md, CONTRIBUTING.md, ISSUE-FIRST.md

**Issue First:** All work begins with a GitHub Issue (see ISSUE-FIRST.md)

---

## Implementation Agent

**Role:** Add or modify SDK API endpoints

**Primary Skill:** `implement-api-endpoint`

### Workflow

1. **Start from GitHub Issue** - Follow Issue First approach (see ISSUE-FIRST.md)
2. **Obtain OpenAPI spec** - Smartsheet public API (<https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json>) or user-provided path
3. **Obtain WireMock mappings location** - smartsheet-sdk-tests repo (<https://github.com/smartsheet/smartsheet-sdk-tests>) or user-provided local path
4. **Create todos from skill checklist** - MANDATORY before any coding (use TodoWrite)
5. **Review gold standard** - Study `tests/mock_api/reports/` before implementing
6. **Implement resource method** - In `smartsheet/{resource}.py`
7. **Write 5 required test types** - Following TESTING.md standards strictly
8. **Verify/create WireMock mappings** - In smartsheet-sdk-tests repo
9. **Update documentation** - In `docs-source/` if required per ADVANCED.md

### Success Criteria

- ✅ All 4 components complete: code, tests, WireMock mappings, documentation
- ✅ Implementation matches OpenAPI spec exactly (every parameter, type, schema)
- ✅ Tests strictly follow TESTING.md standards (no exceptions)
- ✅ Tests match gold standard patterns in `tests/mock_api/reports/`
- ✅ Python 3.7 compatibility verified (no 3.8+ features)
- ✅ Type definitions exist for new endpoints

### Key Requirements

**CANNOT PROCEED without:**

- OpenAPI spec obtained and verified
- WireMock mappings location obtained
- Todos created from skill checklist (no exceptions)
- Gold standard reviewed (`tests/mock_api/reports/`)

**MANDATORY:**

- Python 3.7 compatibility (no walrus operator `:=`, no positional-only `/`, no 3.8+ TypedDict/Literal)
- Type definitions for new endpoints
- All 5 test types (or 4 if required_properties N/A)
- Whole-object assertions: `assert response.to_dict() == {...}` (NOT property-by-property)
- Request body assertions for POST/PUT/PATCH in `all_response_properties` test
- Tests match gold standard patterns exactly (not just similar)

### Common Pitfalls to Avoid

- ❌ Starting implementation without OpenAPI spec verification
- ❌ Starting implementation without WireMock mappings location
- ❌ Skipping todo creation ("quick implementation")
- ❌ Not reviewing gold standard before implementing
- ❌ Stopping at implementation (~20% of work - tests and docs still needed)
- ❌ Property-by-property assertions (allows extra properties to creep in)
- ❌ Missing request body assertions for POST/PUT/PATCH
- ❌ Using Python 3.8+ features (must support 3.7)
- ❌ Tests look "similar" to gold standard (must match EXACTLY)

### Execution Details

See `.claude/skills/implement-api-endpoint/SKILL.md` for:

- Complete step-by-step checklist
- OpenAPI spec verification requirements
- WireMock mappings verification requirements
- Code examples and patterns
- All 5 required test types with examples
- Common mistakes and red flags

---

## Review Agent

**Role:** Review PRs that add or modify API endpoints

**Primary Skill:** `review-api-endpoint`

### Workflow

1. **Obtain OpenAPI spec** - Smartsheet public API (<https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json>) or user-provided path
2. **Obtain WireMock mappings location** - smartsheet-sdk-tests repo (<https://github.com/smartsheet/smartsheet-sdk-tests>) or user-provided local path
3. **Verify implementation matches spec exactly** - Every parameter, type, request/response schema
4. **Verify WireMock mappings exist and match spec** - Check mapping files in repo
5. **Open gold standard for side-by-side comparison** - `tests/mock_api/reports/`
6. **Verify all 5 test types exist** - Not just count, verify quality
7. **Verify tests match gold standard patterns EXACTLY** - Same structure, same assertion style
8. **Verify assertion patterns** - Whole-object (`.to_dict() == {...}`), NOT property-by-property
9. **Verify documentation updates** - Per ADVANCED.md requirements
10. **Approve or request changes** - Based on strict checklist compliance

### Success Criteria

- ✅ OpenAPI spec verified
- ✅ WireMock mappings verified
- ✅ Implementation matches spec exactly
- ✅ Tests match gold standard patterns (side-by-side comparison done)
- ✅ All 4 components present and correct
- ✅ Tests strictly follow TESTING.md standards
- ✅ Python 3.7 compatibility verified
- ✅ Type definitions exist for new endpoints

### Key Requirements

**CANNOT APPROVE without (non-negotiable):**

- OpenAPI spec obtained and implementation verified against it
- WireMock mappings obtained and verified
- Side-by-side comparison with gold standard (`tests/mock_api/reports/`)
- Strict TESTING.md compliance verification

**MUST VERIFY:**

- Implementation matches spec exactly (not "roughly")
- Tests match gold standard patterns exactly (not "similar")
- All 5 test types exist with correct patterns
- Whole-object assertions (no property-by-property)
- Request body assertions for POST/PUT/PATCH
- Python 3.7 compatibility (no 3.8+ features)
- Type definitions for new endpoints

### Automatic Rejection Criteria (MUST block merge)

- ❌ No OpenAPI spec provided or not verified
- ❌ No WireMock mappings provided or not verified
- ❌ Implementation doesn't match spec (parameters, types, schemas)
- ❌ Response/request schemas don't match spec
- ❌ Missing type definitions for new endpoints
- ❌ Python 3.8+ features used (must be 3.7 compatible)
- ❌ Tests don't match gold standard patterns
- ❌ Missing any required test type
- ❌ Tests don't follow TESTING.md standards
- ❌ Property-by-property assertions present
- ❌ Missing request body assertions (POST/PUT/PATCH)
- ❌ Incomplete type safety checks (must check wrapper AND inner type)

### Review Anti-Patterns

**These thoughts mean STOP - review is incomplete:**

- "I don't need to check the spec" - Spec verification is MANDATORY
- "I don't need to check WireMock mappings" - Mappings verification is MANDATORY
- "I didn't compare to reports tests" - Gold standard comparison is MANDATORY
- "Tests look similar to reports" - Must match EXACTLY, not just similar
- "Implementation looks right" - Must verify against spec, not intuition
- "Spec roughly matches" - Must match EXACTLY, not roughly
- "Mappings probably exist" - Must verify, not assume
- "Tests pass, looks good" - Check assertion patterns, not just pass/fail
- "Tests don't strictly follow TESTING.md but close enough" - Standards are MANDATORY

### Execution Details

See `.claude/skills/review-api-endpoint/SKILL.md` for:

- Complete review checklist
- OpenAPI spec verification steps
- WireMock mappings verification steps
- Test quality checks
- Anti-pattern detection
- Example review comments

---

## Skill References

**Location:** `.claude/skills/`

### implement-api-endpoint

**Path:** `.claude/skills/implement-api-endpoint/SKILL.md`

**Contains:**

- 4-part implementation workflow (code, tests, mappings, docs)
- OpenAPI spec verification checklist
- WireMock mappings verification checklist
- 5 required test types with complete examples
- Assertion pattern requirements
- Common mistakes and red flags
- Gold standard references (`tests/mock_api/reports/`)

### review-api-endpoint

**Path:** `.claude/skills/review-api-endpoint/SKILL.md`

**Contains:**

- Systematic review checklist
- OpenAPI spec verification requirements
- WireMock mappings verification requirements
- Test quality assessment criteria
- Assertion pattern checks
- Automatic rejection criteria
- Example review comments

---

## Supporting Documentation

### TESTING.md

**Purpose:** Mock API test standards (MANDATORY compliance)

**Key content:**

- 5 required test types for every endpoint
- Whole-object assertion patterns
- Request body assertion requirements (POST/PUT/PATCH)
- Gold standard reference (`tests/mock_api/reports/`)

### ADVANCED.md

**Purpose:** Advanced SDK patterns and requirements

**Key content:**

- Resource module organization
- Documentation requirements (when docs-source updates needed)
- Delegation patterns

### CONTRIBUTING.md

**Purpose:** General contribution guidelines

**Key content:**

- Documentation file mappings
- Sphinx build instructions
- Contribution workflow

### ISSUE-FIRST.md

**Purpose:** Issue-first development methodology

**Key content:**

- Why issues are required before code
- How to write quality issues for agents
- Examples of well-written issues

### RELEASE.md

**Purpose:** Release procedure — single source of truth for cutting a new SDK version

**Key content:**

- Semver decision rules
- CHANGELOG update pattern
- GitHub Release and tag creation
- PyPI verification

---

## Release Agent

**Role:** Cut a new SDK release

**Primary Skill:** `releasing-smartsheet-python-sdk`

### Skill Reference

**Skill file:** `.claude/skills/releasing-smartsheet-python-sdk/SKILL.md`

**Full procedure:** `RELEASE.md` in the repository root — single source of truth for every step, decision rule, and checklist item.

### When to Use

Use the Release Agent when:

- User asks to cut a release or publish a new version
- Accumulated changes on `mainline` need to be shipped
- A hotfix needs to be released urgently

Do NOT use for:

- Implementing features or fixing bugs (merge those first)
- CI or tooling changes without a version change

---

## Quick Reference

### OpenAPI Spec Location

<https://developers.smartsheet.com/_spec/api/smartsheet/openapi.json>

### WireMock Mappings Location

<https://github.com/smartsheet/smartsheet-sdk-tests>

### Gold Standard Tests

`tests/mock_api/reports/` - All tests must match these patterns exactly

### Python Compatibility

Python 3.7+ (no 3.8+ features: `:=`, `/`, TypedDict, Literal)

### Test Types (All 5 Required)

1. `test_{method}_generated_url_is_correct`
2. `test_{method}_all_response_properties`
3. `test_{method}_required_response_properties` (if applicable)
4. `test_{method}_error_4xx`
5. `test_{method}_error_5xx`

### Assertion Pattern

✅ `assert response.to_dict() == {...}`  
❌ `assert response.id == 123; assert response.name == "test"`
