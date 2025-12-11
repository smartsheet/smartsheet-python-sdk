#!/usr/bin/env bash
set -euo pipefail

# Run live integration tests against real Smartsheet API (only run locally).
# Usage: SMARTSHEET_ACCESS_TOKEN="token" ./scripts/run-live-tests.sh

if [ -z "${SMARTSHEET_ACCESS_TOKEN-}" ]; then
  echo "SMARTSHEET_ACCESS_TOKEN is not set. Aborting." >&2
  echo "Set SMARTSHEET_ACCESS_TOKEN only on your local machine or CI as a secret." >&2
  exit 1
fi

PYTEST_ARGS=${1-""}

echo "Running integration tests against the live API (only run locally)..."
python -m pytest tests/integration $PYTEST_ARGS -q

echo "Integration tests completed.
