#!/usr/bin/env bash

set -eo pipefail

python -m AkvoResponseGrouper.cli.migrate -c ./sources/category.json

pytest -vvv -rP
