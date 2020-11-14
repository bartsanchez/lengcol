#!/bin/bash
set -o pipefail
set -o nounset

export ENV=test

make build
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d web run_migrations
sleep 5
docker-compose -f docker-compose.yml -f docker-compose.test.yml run test
make stop
