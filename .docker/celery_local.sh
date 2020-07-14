#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset

RABBITMQ="tcp://${CLOUDAMQP_URL#*@}"
HOST_AND_DB=${DATABASE_URL#*@}
DB=${HOST_AND_DB%/*}
POSTGRES="tcp://${DB}"

dockerize -wait "${RABBITMQ}" -wait "${POSTGRES}" -timeout 30s

celery -A config.celery worker --loglevel=INFO -B
