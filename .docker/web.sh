#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset

REDIS_NO_DB=${REDIS_URL#*/}
REDIS="tcp:/${REDIS_NO_DB}"
HOST_AND_DB=${DATABASE_URL#*@}
DB=${HOST_AND_DB%/*}
POSTGRES="tcp://${DB}"

dockerize -wait "${REDIS}" -wait "${POSTGRES}"

NEW_RELIC_APP_NAME=web newrelic-admin run-program uwsgi --ini /home/app/.docker/uwsgi.ini
