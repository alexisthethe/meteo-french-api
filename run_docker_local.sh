#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
CMD=$@  # to execute another command rather than running the app (ex: '/bin/sh' to investigate or test)

docker build -t meteofrenchapi:dev $SCRIPT_DIR
docker run -ti --rm --env-file .env.dev --env-file .env.secret -v $(pwd):/root/app -w /root/app -p 8000:8000 meteofrenchapi:dev $CMD
