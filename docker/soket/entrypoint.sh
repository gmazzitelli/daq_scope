#!/bin/sh
if [ -z ${REMOTE_USER} ]; then
    REMOTE_USER=root
fi
if [ -z ${REMOTE_IP} ]; then
    REMOTE_IP=spaip.lnf.infn.it
fi
env
chmod 600 /root/.ssh/id_rsa
# Esegui il comando SSH per creare il tunnel SOCKS
ssh -Nv -o StrictHostKeyChecking=no -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa -D 0.0.0.0:1080 ${REMOTE_USER}@${REMOTE_IP} -i /root/.ssh/id_rsa
