#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

APP_PATH="/opt/apps/lengcol"
DOCKER_COMPOSE="${APP_PATH}/docker-compose.yml"
DOCKER_COMPOSE_PROD="${APP_PATH}/docker-compose.prod.yml"
DOCKER_COMPOSE_FILES="-f ${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PROD}"
BACKUP_CMD="pg_dump db -U postgres"
BACKUP_PATH="/data/backups/db"
BACKUP_DEST_FILE="${BACKUP_PATH}/$(date +%Y%m%d)_db_backup.gz"

docker compose ${DOCKER_COMPOSE_FILES} exec -T db ${BACKUP_CMD} | gzip > ${BACKUP_DEST_FILE}
