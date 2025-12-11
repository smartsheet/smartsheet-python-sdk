# AGENT Tasks — Smartsheet Python SDK

This document lists small, safe tasks and developer workflows that an AI agent can perform in this repository.

General rules for agents:
- Always start from an Issue (see ISSUE-FIRST.md).
- Keep PRs small and focused. Include tests and docs for all behavior changes.
- Never commit secrets (API tokens); use `TEST_*` placeholder variables and mocked test cases.

Safe tasks agents can perform:
- Fix typos in docs and docstrings.
- Add or update unit tests and mock API tests using WireMock mappings.
- Add or improve Sphinx docstrings / docs-source entries.
- Bump dev/test dependencies (Open a PR to update dependency in `pyproject.toml`).
- Add utility helper functions in `tests/mock_api/` to reduce duplication (with tests).

How to run tests locally (mock + WireMock):
```bash
# Fetch the mock API repo once (or the script below does it for you):
git clone https://github.com/smartsheet/smartsheet-sdk-tests.git
cd smartsheet-sdk-tests
docker compose -f docker-compose.yml up -d --wait
cd -
# Run only mock_api tests
python -m pytest tests/mock_api -q
```

Scripts
------
There are helper scripts under `scripts/` to make this more reproducible:

```bash
chmod +x scripts/run-mock-tests.sh scripts/run-live-tests.sh
./scripts/run-mock-tests.sh
```

Makefile targets
----------------
You can also run the same commands via `make` if you prefer:

```bash
make run-mock-tests
make run-live-tests
```



How to run live integration tests (use only for local debugging):
```bash
export SMARTSHEET_ACCESS_TOKEN="<real_token>" # DO NOT COMMIT
python -m pytest tests/integration -q
```

How to add a WireMock mapping for tests (summary):
1. Update `smartsheet-sdk-tests` with a new mapping and response JSON.
2. Add an integration in `tests/mock_api/` pointing to that mapping by `x-test-name`.
3. Add a test that calls `get_mock_api_client(test_name, request_id)`.

If you'd like, I can also add local scripts to make these steps reproducible and a GitHub Actions snippet for local developers.
