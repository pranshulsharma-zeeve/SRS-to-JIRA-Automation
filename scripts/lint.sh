#!/usr/bin/env bash
set -euo pipefail

python -m py_compile frontend/src/*.py backend/src/*.py
