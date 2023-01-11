#!/usr/bin/env bash

set -eo pipefail

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

pytest -vvv -rP
