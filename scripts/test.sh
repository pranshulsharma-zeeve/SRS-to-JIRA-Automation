#!/usr/bin/env bash
set -euo pipefail

python -m unittest discover -s frontend/tests -p "test_*.py"
python -m unittest discover -s backend/tests -p "test_*.py"
