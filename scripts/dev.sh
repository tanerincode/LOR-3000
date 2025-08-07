#!/usr/bin/env bash
set -euo pipefail
export $(grep -v '^#' .env 2>/dev/null | xargs -I{} echo {}) || true

export PYTHONPATH=src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
