# Contributing to Smartsheet Python SDK

## Did you find a bug?

- **Send all security related bugs to our maintainer email, <sdk-python@smartsheet.com>**.

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/smartsheet/smartsheet-python-sdk/issues).

- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/smartsheet/smartsheet-python-sdk/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **[MRE code sample](https://stackoverflow.com/help/minimal-reproducible-example)** or an **executable test case** demonstrating the expected behavior that is not occurring. If possible please also note if this issue concerns the API itself or just the Python SDK.

## Did you write a patch that fixes a bug?

- Open a new GitHub pull request with the patch.

- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

- A maintainer should review your PR within the next few days. If the PR has been dormant for more than a week, consider sending an email to <sdk-python@smartsheet.com>

## Did you fix whitespace, format code, or make a purely cosmetic patch?

Changes that are cosmetic in nature and do not add anything substantial to the stability, functionality, or testability may take longer to review, but are still welcome.

## Do you intend to add a new feature or change an existing one?

- Suggest your change as an issue with the label #enhancement. Make sure that your new feature description outlines why this would be helpful for users, and how difficult a change it would be to make.

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
  cd docs-source
  make html
  ```

- The built documentation will be in `docs-source/_build/html/`. Open `index.html` in a browser to review your changes.

## Running Tests

- To run the test suite, use the following command:

  ```bash
  python -m pytest tests/
  ```

- For integration tests, you'll need to set up your Smartsheet API access token as an environment variable:

  ```bash
  export SMARTSHEET_ACCESS_TOKEN=your_token_here
  ```

## Do you have questions about the source code or using the SDK?

- For general information on the API and its uses, see the [Smartsheet API Reference](https://smartsheet.redoc.ly/)

- For information on the Python SDK, see the [Smartsheet Python SDK Documentation](https://github.com/smartsheet/smartsheet-python-sdk#readme) or review the [basic](https://github.com/smartsheet/smartsheet-python-sdk#readme) and [advanced](https://github.com/smartsheet/smartsheet-python-sdk/blob/master/ADVANCED.md) READMEs!

- Github issues can also be used for questions on using the Python SDK specifically.

Thanks!

Smartsheet Python SDK Team
