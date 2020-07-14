#!/usr/bin/env sh

docker login \
  -u ${CI_REGISTRY_USER} \
  -p ${CI_REGISTRY_PASSWORD} \
  ${CI_REGISTRY}

docker pull \
  ${IMAGE}

docker run -d \
  --name "postgres" \
  --env "POSTGRES_DB=${POSTGRES_DB}" \
  --env "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" \
  --env "POSTGRES_USER=${POSTGRES_USER}" \
  "postgres:alpine"

docker run -d \
  --name "redis" \
  "redis:alpine"

docker run -d \
  --name "rabbitmq" \
  "rabbitmq:alpine"

docker run -i \
  --name "tester" \
  --link "postgres:postgres" \
  --link "redis:redis" \
  --env "CLOUDAMQP_URL=amqp://guest:guest@rabbitmq:5672" \
  --env "COVERAGE_FILE=output/.coverage" \
  --env "DATABASE_URL=${DATABASE_URL}" \
  --env "DJANGO_SETTINGS_MODULE=config.settings.test" \
  --env "REDIS_URL=redis://redis:6379" \
  --env "SECRET_KEY=ASECRETTESTKEY" \
  ${IMAGE} \
  pytest --cov-report html:output/coverage --cov-report xml:output/coverage/coverage.xml --cov-report term --junitxml=output/junit.xml --cov=.

EXIT=$?

docker cp tester:/home/app/ops_status/output/. ./ops_status/output/

docker rm tester
docker stop postgres && docker rm postgres
docker stop redis && docker rm redis

exit ${EXIT}
