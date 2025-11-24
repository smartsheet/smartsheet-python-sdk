# Issue First Approach for Smartsheet Python SDK

## What is "Issue First"?

The "Issue First" approach is a collaborative development methodology where **all contributions to the Smartsheet Python SDK must begin with a GitHub Issue** before any code changes are made. This means that whether you're fixing a bug, adding a new feature, or improving documentation, you first create or identify an existing issue that describes what needs to be done.

## Why Issue First Matters for Cloud Agents

With the integration of Roo Code Cloud Agents in the Smartsheet Python SDK repository, the Issue First approach becomes even more critical. Here's why:

### 1. **Clear Communication with AI Agents**

Cloud Agents are AI-powered assistants that can understand natural language and translate it into code changes. A well-written GitHub Issue serves as a **high-quality prompt** that gives the Cloud Agent all the context it needs to:

- Understand the problem or feature request
- Identify which parts of the Smartsheet Python SDK codebase need to be modified
- Generate appropriate Python code that follows the SDK's patterns and conventions
- Create comprehensive tests and documentation

### 2. **Structured Problem Definition**

Issues provide a structured format that helps both humans and AI agents understand:

- **What** needs to change (the goal)
- **Why** it needs to change (the motivation)
- **How** it should work (expected behavior)
- **Context** about the Smartsheet Python SDK codebase

### 3. **Trackable Progress**

Issues create a clear audit trail of:

- What work was requested
- Who is working on it (human or Cloud Agent)
- The discussion and decisions made
- The resulting code changes via linked Pull Requests

### 4. **Quality Control**

By requiring an issue first, we ensure that:

- The proposed change aligns with the SDK's goals and architecture
- Duplicate work is avoided
- The community can provide input before code is written
- Cloud Agents have sufficient context to generate high-quality code

## How to Use Issue First with Roo Cloud Agents

### Step 1: Create a Quality Issue

When creating an issue that will be used by a Roo Cloud Agent, provide comprehensive details:

#### For Bug Reports

```markdown
**Description**: Clear description of the bug in the Smartsheet Python SDK

**Steps to Reproduce**:
1. Import the SDK: `import smartsheet`
2. Call the specific method: `client.Sheets.get_sheet(sheet_id)`
3. Observe the error

**Expected Behavior**: What should happen when using the SDK

**Actual Behavior**: What actually happens

**Environment**:
- SDK Version: (e.g., 3.0.0)
- Python Version: (e.g., 3.9.0)
- Operating System: (e.g., Ubuntu 22.04)

**Code Sample** (if applicable):
```python
import smartsheet
client = smartsheet.Smartsheet('your_token')
# Your code that demonstrates the issue
\`\`\`

**Additional Context**: Any relevant details about the Smartsheet API, error messages, or stack traces
\`\`\`

#### For Feature Requests

```markdown
**Feature Description**: Clear description of the new functionality needed in the Smartsheet Python SDK

**Use Case**: Why this feature is needed and how it will be used

**Proposed API**:
```python
# Example of how the feature would be used
client.Sheets.new_method(parameters)
```

**Smartsheet API Reference**: Link to relevant Smartsheet API documentation if applicable

**Implementation Considerations**:

- Which SDK modules would be affected (e.g., `smartsheet/sheets.py`, `smartsheet/models/`)
- Any dependencies or related features
- Backwards compatibility concerns

**Alternatives Considered**: Other approaches that were considered
\`\`\`

#### For Documentation Improvements

```markdown
**Documentation Issue**: What documentation is missing, unclear, or incorrect

**Location**: Which file or section needs improvement (e.g., `README.md`, `ADVANCED.md`)

**Suggested Improvement**: What should be added or changed

**Context**: Why this documentation is important for SDK users
\`\`\`

### Step 2: Let the Cloud Agent Work

Once your issue is well-defined:

1. **The Cloud Agent reads your issue** as its primary prompt
2. **It analyzes the Smartsheet Python SDK codebase** to understand:
   - Existing patterns and conventions
   - Related code that may need updates
   - Test files that need modifications
   - Documentation that should be updated

3. **It generates the necessary changes**:
   - Python code following the SDK's style
   - Unit tests using the project's testing framework
   - Updated documentation
   - Appropriate error handling

4. **It creates a Pull Request** linked to your issue with all the changes

### Step 3: Review and Iterate

After the Cloud Agent creates a PR:

1. Review the generated code for correctness and quality
2. Test the changes locally with the Smartsheet API
3. Provide feedback in the PR comments
4. The Cloud Agent can iterate based on your feedback
5. Once approved, the changes are merged

## Best Practices for Writing Issues

### Be Specific and Detailed

**Poor Issue**: "Fix the sheet method"

**Good Issue**: "Fix TypeError in `Sheets.get_sheet()` when sheet contains cell links - occurs when a sheet has cells with links to other sheets, the SDK raises a TypeError during deserialization of the Cell model"

### Include Code Examples

Show how the SDK is being used and what's not working:

```python
import smartsheet

client = smartsheet.Smartsheet(access_token='your_token')

# This raises an error
sheet = client.Sheets.get_sheet(1234567890)
print(sheet.rows[0].cells[0].value)  # TypeError here
```

### Reference Smartsheet API Documentation

Link to relevant Smartsheet API documentation to help the Cloud Agent understand the expected behavior:

```markdown
According to the [Smartsheet API documentation for Get Sheet](https://developers.smartsheet.com/api/smartsheet/openapi/sheets/get-sheet),
the response should include...
```

### Specify the Scope

Be clear about what should and shouldn't be changed:

```markdown
**In Scope**:
- Update the `Cell` model in `smartsheet/models/cell.py`
- Add handling for cell link objects
- Update tests in `tests/mock_api/test_mock_api_sheets.py`

**Out of Scope**:
- Changes to other models
- API authentication changes
```

### Tag Appropriately

Use GitHub labels to help categorize your issue:

- `bug` - Something isn't working correctly
- `enhancement` - New feature or improvement
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed

## Examples of Well-Written Issues

### Example 1: Bug Report

```markdown
**Title**: Cell deserialization fails when cell contains hyperlink with null url

**Description**:
When using the Smartsheet Python SDK to retrieve a sheet that contains cells with hyperlinks
where the url property is null, the SDK raises an AttributeError during deserialization.

**Steps to Reproduce**:

1. Create a sheet in Smartsheet with a cell containing a hyperlink with no URL
2. Use the SDK to get the sheet:

\`\`\`python
import smartsheet
client = smartsheet.Smartsheet('token')
sheet = client.Sheets.get_sheet(sheet_id)
\`\`\`

3. Observe the AttributeError

**Expected Behavior**:
The SDK should handle null hyperlink URLs gracefully, either by setting the url to None
or providing a default value.

**Actual Behavior**:

\`\`\`text
AttributeError: 'NoneType' object has no attribute 'strip'
  File "smartsheet/models/hyperlink.py", line 45, in __init__
\`\`\`

**Environment**:

- SDK Version: 2.105.1
- Python Version: 3.9.7
- OS: macOS 12.6

**Smartsheet API Reference**:
<https://developers.smartsheet.com/api/smartsheet/openapi/sheets/get-sheet>

\`\`\`

### Example 2: Feature Request

```markdown
**Title**: Add support for Sheet Summary Fields API

**Description**:
The Smartsheet Python SDK currently does not support the Sheet Summary Fields API endpoints.
This feature would allow users to programmatically read and update sheet summary fields.

**Use Case**:
Users need to automate updating project metadata stored in sheet summaries, such as
project status, start dates, and custom KPIs.

**Proposed API**:

\`\`\`python
# Get summary fields
summary = client.Sheets.get_sheet_summary(sheet_id)
for field in summary.fields:
    print(f"{field.title}: {field.value}")

# Update a summary field
client.Sheets.update_summary_field(
    sheet_id=sheet_id,
    field_id=field_id,
    value="Updated value"
)
\`\`\`

**Smartsheet API Reference**:

- <https://developers.smartsheet.com/api/smartsheet/openapi/sheetsummary/list-summary-fields>
- <https://developers.smartsheet.com/api/smartsheet/openapi/sheetsummary/get-sheet-summary>

**Implementation Considerations**:

- Add new methods to `smartsheet/sheets.py`
- Create `SummaryField` model in `smartsheet/models/`
- Add tests to verify API integration
- Update documentation in `README.md` or `ADVANCED.md`

**Related Issues**: None

**Alternatives Considered**:
Using direct API calls with the `Passthrough` module, but a native SDK implementation
would provide better type hints and error handling.
\`\`\`

## Conclusion

The Issue First approach, combined with Roo Code Cloud Agents, creates a powerful workflow for contributing to the Smartsheet Python SDK. By writing clear, detailed issues, you provide Cloud Agents with the context they need to generate high-quality code changes. This approach ensures that:

- All changes are well-documented and justified
- The community can provide input and avoid duplicate work
- Cloud Agents have the information they need to be effective
- The SDK maintains high quality and consistency

Remember: **A well-written issue is the foundation for successful automation with Cloud Agents.**
