#!/usr/bin/env bash
# Test that e2e routing works after removing /code/ prefix from tests/templates
# Usage: ./tools/test-router-fix.sh

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d venv ]; then
    echo "No venv found; run create-venv.sh first" >&2
    exit 1
fi

source venv/bin/activate

python -m unittest test.test_end_to_end -v
