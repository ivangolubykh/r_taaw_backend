#!/bin/bash
set -e

# Determine absolute path to the root of the project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# If passed --html, generate and attempt to open HTML report
if [[ "$1" == "--html" ]]; then
    coverage html
    xdg-open htmlcov/index.html 2>/dev/null || open htmlcov/index.html || \
        echo "HTML report generated at htmlcov/index.html"
else
    # Show terminal coverage report with uncovered lines
    coverage report -m
fi
