# Async PoC Tests

This directory contains comprehensive tests for the async Smartsheet Python SDK proof-of-concept implementation.

## Test Files

### 1. `test_async_poc.py`

Core tests for the async PoC implementation covering:

- **AsyncSmartsheet Client Tests**
  - Client initialization and configuration
  - Context manager lifecycle (`async with`)
  - Manual resource cleanup (`aclose()`)
  - Environment variable configuration
  - Error handling preferences

- **AsyncSheets.add_rows() Tests**
  - Successful row addition
  - Single row vs. list of rows
  - Error responses
  - Exception handling when enabled

- **AsyncWorkspaces.list_workspaces() Tests**
  - Successful workspace listing
  - Token-based pagination (recommended)
  - Legacy pagination (deprecated)
  - Parameter validation
  - Error handling

- **Concurrent Operations Tests**
  - Multiple concurrent add_rows operations
  - Multiple concurrent list_workspaces operations
  - Mixed concurrent operations (reads and writes)

- **Retry Logic Tests**
  - Rate limit retry (error code 4003)
  - No retry on client errors (4xx)
  - Max retry time exceeded

- **Resource Cleanup Tests**
  - Context manager cleanup on exceptions
  - Multiple close calls safety

### 2. `test_async_framework_integration.py`

Async framework integration tests demonstrating event loop compatibility:

- **Event Loop Compatibility Tests**
  - Non-blocking concurrent operations
  - Event loop responsiveness during I/O
  - Performance characteristics of async operations

- **Async Service Pattern Tests**
  - Service handler pattern simulation
  - Request queue processing with workers
  - Controlled concurrency

- **Error Handling Tests**
  - Partial failures in concurrent operations
  - Timeout handling
  - Graceful error recovery

- **Resource Management Tests**
  - Connection pooling under load
  - Graceful shutdown with pending operations

## Setup

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install the package with test dependencies**:

   ```bash
   pip install -e ".[test]"
   ```

   This installs:
   - `pytest` - Test framework
   - `pytest-asyncio>=0.21.0` - Async test support
   - `coverage` - Code coverage reporting
   - Other test utilities

3. **Verify installation**:

   ```bash
   python -m pytest --version
   ```

## Running Tests

### Run All Async Tests

```bash
# Run both test files
pytest tests/test_async_poc.py tests/test_async_framework_integration.py -v

# Or run all tests in the tests directory
pytest tests/ -v
```

### Run Specific Test File

```bash
# Run only core async PoC tests
pytest tests/test_async_poc.py -v

# Run only async framework integration tests
pytest tests/test_async_framework_integration.py -v
```

### Run Specific Test Class or Function

```bash
# Run a specific test class
pytest tests/test_async_poc.py::TestAsyncSmartsheetClient -v

# Run a specific test function
pytest tests/test_async_poc.py::TestAsyncSmartsheetClient::test_client_initialization -v

# Run tests matching a pattern
pytest tests/test_async_poc.py -k "concurrent" -v
```

### Run with Coverage

```bash
# Generate coverage report
pytest tests/test_async_poc.py tests/test_async_framework_integration.py --cov=smartsheet --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
# or
xdg-open htmlcov/index.html  # On Linux
# or
start htmlcov/index.html  # On Windows
```

### Run with Different Output Formats

```bash
# Verbose output
pytest tests/test_async_poc.py -v

# Very verbose output (shows test docstrings)
pytest tests/test_async_poc.py -vv

# Show print statements
pytest tests/test_async_poc.py -v -s

# Show only failures
pytest tests/test_async_poc.py -v --tb=short

# Show summary of all test outcomes
pytest tests/test_async_poc.py -v -ra
```

## Test Architecture

### Mocking Strategy

All tests use mocked HTTP responses to avoid making real API calls:

- **`mock_httpx_response` fixture**: Creates mock `httpx.Response` objects with configurable:
  - Status codes
  - JSON response data
  - Response delays (for timing tests)
  - Headers

- **`AsyncMock`**: Used to mock async methods like `session.send()`

- **`patch`**: Used to replace client session with mocked version

### Fixtures

- **`mock_access_token`**: Provides a test access token
- **`async_client`**: Creates and cleans up an `AsyncSmartsheet` client
- **`mock_httpx_response`**: Factory for creating mock HTTP responses

### Async Test Patterns

Tests use `pytest-asyncio` markers:

```python
@pytest.mark.asyncio
async def test_example(async_client):
    result = await async_client.Workspaces.list_workspaces()
    assert isinstance(result, IndexResult)
```

## Test Coverage

The test suite covers:

- ✅ Client initialization and configuration
- ✅ Context manager lifecycle
- ✅ AsyncSheets.add_rows() method
- ✅ AsyncWorkspaces.list_workspaces() method
- ✅ Concurrent operations (asyncio.gather)
- ✅ Retry logic and backoff
- ✅ Error handling (with and without exceptions)
- ✅ Resource cleanup
- ✅ Event loop non-blocking behavior
- ✅ Async service patterns
- ✅ Connection pooling
- ✅ Graceful shutdown

## Performance Tests

The async framework integration tests include timing assertions to verify non-blocking behavior:

```python
# Example: Verify concurrent execution is faster than sequential
start_time = time.time()
results = await asyncio.gather(*tasks)
elapsed_time = time.time() - start_time

# With 5 concurrent requests at 0.1s each:
# Sequential: 5 * 0.1 = 0.5s
# Concurrent: ~0.1s
assert elapsed_time < 0.3  # Allows overhead
```

## Troubleshooting

### Import Errors

If you see import errors like `ModuleNotFoundError: No module named 'smartsheet'`:

```bash
# Make sure you installed the package in editable mode
pip install -e .

# Or with test dependencies
pip install -e ".[test]"
```

### pytest-asyncio Warnings

If you see warnings about asyncio mode:

```bash
# Add to pytest.ini or pyproject.toml:
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Mock Not Working

If mocks aren't being applied:

```python
# Ensure you're patching the right object
with patch.object(async_client, '_session') as mock_session:
    # Not: patch('smartsheet.async_smartsheet.httpx.AsyncClient')
```

### Tests Hanging

If tests hang indefinitely:

- Check for missing `await` keywords
- Verify all async fixtures are properly cleaned up
- Use `pytest --timeout=30` to set a timeout

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Async PoC

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[test]"
    
    - name: Run async tests
      run: |
        pytest tests/test_async_poc.py tests/test_async_framework_integration.py -v --cov=smartsheet
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Future Test Additions

As the async implementation expands beyond the PoC, add tests for:

- Additional async API methods (get_sheet, update_row, etc.)
- Streaming operations
- Webhook handling
- Batch operations
- More complex error scenarios
- Performance benchmarks
- Memory leak detection

## Contributing

When adding new async functionality:

1. Add corresponding tests to `test_async_poc.py`
2. Add integration tests to `test_async_framework_integration.py` if relevant
3. Use mocks - never make real API calls in tests
4. Include docstrings explaining what each test validates
5. Follow existing test patterns and naming conventions
6. Ensure tests are deterministic (no random failures)
7. Add timing assertions for performance-critical features

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [httpx documentation](https://www.python-httpx.org/)
- [Smartsheet API documentation](https://smartsheet.redoc.ly/)
