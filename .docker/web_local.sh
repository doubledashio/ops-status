#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset

REDIS="tcp:/${REDIS_URL#*/}"
HOST_AND_DB=${DATABASE_URL#*@}
DB=${HOST_AND_DB%/*}
POSTGRES="tcp://${DB}"

dockerize -wait "${REDIS}" -wait "${POSTGRES}" -timeout 30s

python /home/app/ops_status/manage.py migrate
python -m ptvsd --host 0.0.0.0 --port 5678 /home/app/ops_status/manage.py runserver 0.0.0.0:${PORT:-5000}
