#!/bin/sh
ID_RSA=/Users/vallis/Projects/rasa-coffee-bot/.app/git/ssh_files/1.key
# Kubernetes tends to reset file permissions on restart. Hence, re-apply the required
# permissions whenever using the key.
chmod 600 $ID_RSA
exec /usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $ID_RSA "$@"
