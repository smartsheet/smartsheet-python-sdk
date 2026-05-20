# Contributing to Smartsheet Python SDK

## Issue First Approach

**All contributions to the Smartsheet Python SDK must begin with a GitHub Issue.** This includes bug fixes, new features, and documentation improvements.

For detailed guidance on creating effective issues that work well with both human reviewers and AI-powered Cloud Agents, see our [Issue First documentation](ISSUE-FIRST.md).

## Development Setup

### Prerequisites

- Python 3.8+ (required for development tooling)
- uv package manager

**Important:** While the smartsheet-python-sdk supports Python 3.7+, development requires Python 3.8+ for the uv tooling. If you need to verify Python 3.7 compatibility, you can use pip in a Python 3.7 environment, but all other development should use uv with Python 3.8+.

### Installing uv

Install uv using one of these methods:

```bash
# Using pip
pip install uv

# Using Homebrew (macOS)
brew install uv

# Using the standalone installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/smartsheet/smartsheet-python-sdk.git
   cd smartsheet-python-sdk
   ```

2. Install all development dependencies:
   ```bash
   uv sync --all-extras
   ```

This creates a virtual environment in `.venv` and installs all dependencies from the lockfile.

## Did you find a bug?

- **Send all security related bugs to our maintainer email, <sdk-python@smartsheet.com>**.

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues).

- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/smartsheet/smartsheet-python-sdk/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **[MRE code sample](https://stackoverflow.com/help/minimal-reproducible-example)** or an **executable test case** demonstrating the expected behavior that is not occurring. If possible please also note if this issue concerns the API itself or just the Python SDK.

## Did you write a patch that fixes a bug?

- **First, ensure there is a GitHub issue** describing the bug (see above).

- Open a new GitHub pull request with the patch, referencing the issue number.

- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number.

- A maintainer should review your PR within the next few days. If the PR has been dormant for more than a week, consider sending an email to <sdk-python@smartsheet.com>

## Did you fix whitespace, format code, or make a purely cosmetic patch?

Changes that are cosmetic in nature and do not add anything substantial to the stability, functionality, or testability may take longer to review, but are still welcome. Please create an issue first describing the cosmetic changes you'd like to make.

## Do you intend to add a new feature or change an existing one?

- **First, create an issue** with the label #enhancement. Make sure that your new feature description outlines why this would be helpful for users, and how difficult a change it would be to make.

- Once the feature is discussed and approved in the issue, you can submit a pull request implementing it.

## Code Style and Quality

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines for Python code.

- Use meaningful variable and function names that clearly describe their purpose.

- Include docstrings for all public modules, functions, classes, and methods following [PEP 257](https://www.python.org/dev/peps/pep-0257/) conventions.

- Run pylint on your code before submitting a PR. The project includes a pylintrc file with project-specific settings.

- Write unit tests for new features and bug fixes. All tests should pass before submitting a PR.

## Documentation

- If your changes affect the public API, you must update the corresponding Sphinx documentation files in `docs-source/`:
  - **API Resources** (modules in `smartsheet/`): Update `docs-source/smartsheet_api.rst`
  - **Models** (classes in `smartsheet/models/`): Update `docs-source/smartsheet_models.rst`
  - **Enums** (enums in `smartsheet/models/enums/`): Update `docs-source/smartsheet_enums.rst`
  - **Types** (type definitions in `smartsheet/types.py`): Update `docs-source/smartsheet_types.rst`
  - **Exceptions** (exceptions in `smartsheet/exceptions.py`): Update `docs-source/smartsheet_exceptions.rst`
  - **General documentation** (installation, quickstart, examples): Update `docs-source/index.rst`

- The documentation uses Sphinx with autodoc to generate API documentation from docstrings. Ensure your docstrings follow Google-style format as configured in `docs-source/conf.py`.

- After making changes to `docs-source/`, you can build the documentation locally to verify your changes:

  ```bash
  uv run sphinx-build -b html docs-source docs-source/_build/html
  ```

- The built documentation will be in `docs-source/_build/html/`. Open `index.html` in a browser to review your changes.

## Running Tests

To run the test suite:

```bash
uv run pytest tests/
```

For integration tests, you'll need to set up your Smartsheet API access token as an environment variable:

```bash
export SMARTSHEET_ACCESS_TOKEN=your_token_here
uv run pytest tests/
```

To run tests with coverage:

```bash
uv run coverage run --source=smartsheet -m pytest
uv run coverage report -m
```

## Common Development Commands

The project uses uv for all development tasks. Here are the most common commands:

```bash
# Install/update dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run pylint smartsheet

# Build the package
uv build

# Update a specific dependency
uv lock --upgrade-package requests

# Update all dependencies
uv lock --upgrade
```

**Note:** The project previously used a Makefile for these commands. That has been replaced by the uv commands above.

## Do you have questions about the source code or using the SDK?

- For general information on the API and its uses, see the [Smartsheet API Reference](https://smartsheet.redoc.ly/)

- For information on the Python SDK, see the [Smartsheet Python SDK Documentation](https://github.com/smartsheet/smartsheet-python-sdk#readme) or review the [basic](https://github.com/smartsheet/smartsheet-python-sdk#readme) and [advanced](https://github.com/smartsheet/smartsheet-python-sdk/blob/master/ADVANCED.md) READMEs!

- Github issues can also be used for questions on using the Python SDK specifically.

Thanks!

Smartsheet Python SDK Team
