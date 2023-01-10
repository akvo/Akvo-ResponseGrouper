#!/usr/bin/env bash

set -eo pipefail

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

alembic upgrade head

find ./AkvoResponseGrouper -maxdepth 0 -empty -exec echo {} is empty. \;

uvicorn main:app --reload --port 5000 --host 0.0.0.0
