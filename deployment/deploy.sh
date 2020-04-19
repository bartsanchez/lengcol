#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

CURRENT_PATH="${BASH_SOURCE%/*}"
HOSTS_FILE="${CURRENT_PATH}/ansible/hosts"
DEPLOY_FILE="${CURRENT_PATH}/ansible/deploy.yml"

ansible-playbook -i ${HOSTS_FILE} ${DEPLOY_FILE} --private-key aws_key_pair.pem --ask-vault-pass
