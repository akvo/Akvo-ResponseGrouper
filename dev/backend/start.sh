#!/usr/bin/env bash

set -euo pipefail

set -eu
pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

alembic upgrade head

uvicorn main:app --reload --port 5000 --host 0.0.0.0