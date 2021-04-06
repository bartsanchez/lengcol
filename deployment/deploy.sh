#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

CURRENT_PATH="${BASH_SOURCE%/*}"
HOSTS_FILE="${CURRENT_PATH}/ansible/hosts"
DEPLOY_FILE="${CURRENT_PATH}/ansible/deploy.yml"

echo $VAULT_PASSWORD > ./vault_password_file.txt

printf '%s\n' "$AWS_KEY_PAIR_PEM_FILE" > ./aws_key_pair.pem
chmod 600 ./aws_key_pair.pem

ansible-playbook -i ${HOSTS_FILE} ${DEPLOY_FILE} --private-key ./aws_key_pair.pem --vault-password-file=./vault_password_file.txt
