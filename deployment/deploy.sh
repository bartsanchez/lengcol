#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

CURRENT_PATH="${BASH_SOURCE%/*}"
HOSTS_FILE="${CURRENT_PATH}/ansible/hosts"
DEPLOY_FILE="${CURRENT_PATH}/ansible/deploy.yml"

echo $VAULT_PASSWORD > ./vault_password_file.txt

ansible-playbook -i ${HOSTS_FILE} ${DEPLOY_FILE} --private-key deployment/aws_key_pair.pem --vault-password-file=./vault_password_file.txt
