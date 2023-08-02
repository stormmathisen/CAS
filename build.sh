#/usr/bin/bash

git clone git@gitlab.stfc.ac.uk:clara-control-room-applications/shared-procedures/machine.git ./lib/machine
docker build -t cas-server -f ./Docker/Dockerfile .