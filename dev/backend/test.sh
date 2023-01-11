#!/usr/bin/env bash

set -eo pipefail

find ./AkvoResponseGrouper -maxdepth 0 -empty -exec echo {} is empty. \;

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

alembic upgrade head

python -m AkvoResponseGrouper.cli.migrate -c ./sources/category.json

pytest -vvv -rP
