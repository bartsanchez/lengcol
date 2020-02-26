#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


ansible-playbook -i ansible/hosts ansible/deploy.yml --private-key aws_key_pair.pem --ask-vault-pass
