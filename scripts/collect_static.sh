#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

APP_EXEC="python3 manage.py"

$APP_EXEC collectstatic --no-input
