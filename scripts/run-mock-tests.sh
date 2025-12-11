#!/usr/bin/env bash
set -euo pipefail

# Run WireMock-based mock API tests for the Smartsheet Python SDK.
# Usage: ./scripts/run-mock-tests.sh [--no-clone]

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
MOCK_REPO_DIR="$ROOT_DIR/smartsheet-sdk-tests"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found; please install Docker Desktop or Docker Engine." >&2
  exit 1
fi

if [ "$1" != "--no-clone" ]; then
  if [ ! -d "$MOCK_REPO_DIR" ]; then
    echo "Cloning smartsheet-sdk-tests into $MOCK_REPO_DIR..."
    git clone https://github.com/smartsheet/smartsheet-sdk-tests.git "$MOCK_REPO_DIR"
  fi
fi

echo "Starting WireMock server via Docker Compose..."
pushd "$MOCK_REPO_DIR" >/dev/null
docker compose -f docker-compose.yml up -d --wait
popd >/dev/null

echo "Running mock API tests..."
python -m pytest tests/mock_api -q

echo "Tearing down WireMock server..."
pushd "$MOCK_REPO_DIR" >/dev/null
docker compose -f docker-compose.yml down
popd >/dev/null

echo "Mock tests completed.
