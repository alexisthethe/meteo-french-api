#!/bin/bash

# Params
IMAGE="alexisthethe/meteo-french-api"

# Constants
SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
# get version of the api from config.py
version_tag=test-autoscale


if [ ! -z ${1} ]; then
    IMAGE=${1}
fi

docker build -t ${IMAGE}:${version_tag} $SCRIPT_DIR
docker push ${IMAGE}:${version_tag}
