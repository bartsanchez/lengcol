#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

export ENV=test

# Prepare system
make build
make start START_SERVICES="web run_migrations"
sleep 5

# Run tests
set +o errexit
make run RUN_SERVICE=test
return_code=$?
set -o errexit

# Down system
make stop

# Exit script
exit $return_code
