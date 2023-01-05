#!/usr/bin/env bash
#shellcheck disable=SC2016

set -eu
DATABASES='demo'

for DB in ${DATABASES}
do
    docker-compose exec -T db bash -c "pg_dump --user akvo --clean --create --format plain ${DB} > /docker-entrypoint-initdb.d/001-init-${DB}.sql;"
    echo "Export ${DB} done"
done
