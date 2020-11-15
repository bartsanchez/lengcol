#!/bin/bash
set -o pipefail
set -o nounset

export ENV=test

make build
make start START_SERVICES="web run_migrations"
sleep 5
make run RUN_SERVICE=test
make stop
