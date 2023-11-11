#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

APP_PATH="/opt/apps/lengcol"
DOCKER_COMPOSE="${APP_PATH}/docker-compose.yml"
DOCKER_COMPOSE_PROD="${APP_PATH}/docker-compose.prod.yml"
DOCKER_COMPOSE_FILES="-f ${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PROD}"

docker compose ${DOCKER_COMPOSE_FILES} up -d web
