#!/bin/bash

# Params
IMAGE="alexisthethe/meteo-french-api"

# Constants
SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
# get version of the api from config.py
version_tag=$(grep " *VERSION *= *" $SCRIPT_DIR/meteofrenchapi/config.py | rev | cut -d" " -f1 | rev | tr -d "'" | tr -d '"')


if [ ! -z ${1} ]; then
    IMAGE=${1}
fi

docker build -t ${IMAGE}:latest $SCRIPT_DIR
docker tag ${IMAGE}:latest ${IMAGE}:${version_tag}
docker push ${IMAGE}:latest
docker push ${IMAGE}:${version_tag}
