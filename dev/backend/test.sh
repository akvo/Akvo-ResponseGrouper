#!/usr/bin/env bash

set -euo pipefail

find ./AkvoResponseGrouper -maxdepth 0 -empty -exec echo {} is empty. \;

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

pwd
ls -la

alembic upgrade head

python -m AkvoResponseGrouper.cli.migrate -c ./sources/category.json

echo "Running tests"
COVERAGE_PROCESS_START=./.coveragerc \
  coverage run --parallel-mode --concurrency=thread,gevent --rcfile=./.coveragerc \
  /usr/local/bin/pytest -vvv -rP



echo "===Coverage==="
coverage combine --rcfile=./.coveragerc
pwd
ls -la


echo "===Reporting==="
coverage report -m --rcfile=./.coveragerc
pwd
ls -la


if [[ -n "${COVERALLS_REPO_TOKEN:-}" ]] ; then
  coveralls
fi
