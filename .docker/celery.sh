#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset

HOST_AND_DB=${DATABASE_URL#*@}
DB=${HOST_AND_DB%/*}
POSTGRES="tcp://${DB}"

dockerize -wait "${POSTGRES}"

NEW_RELIC_APP_NAME=celery newrelic-admin run-program celery -A config.celery worker --loglevel=ERROR -B
