#!/bin/bash
set -e

# Determine absolute path to the root of the project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Run pytest and collect coverage data (does NOT display coverage report)
pytest --ds=r_taaw_backend.settings --cov=. --cov-report= "$@"
