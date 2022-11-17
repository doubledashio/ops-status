#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset

REDIS="tcp:/${REDIS_URL#*/}"
HOST_AND_DB=${DATABASE_URL#*@}
DB=${HOST_AND_DB%/*}
POSTGRES="tcp://${DB}"

dockerize -wait "${REDIS}" -wait "${POSTGRES}"

python /home/app/ops_status/manage.py qcluster
