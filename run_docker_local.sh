#!/bin/bash

# Params
LOCAL_PORT=8000

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
CMD=$@  # to execute another command rather than running the app (ex: '/bin/sh' to investigate or test)

docker build -t meteofrenchapi:dev $SCRIPT_DIR
echo ""
echo "Binding on local port $LOCAL_PORT => visit http://localhost:$LOCAL_PORT"
echo ""
PORT=$(grep " *PORT *= *" $SCRIPT_DIR/.env.dev | cut -d"=" -f2 | xargs)
docker run -ti --rm --env-file $SCRIPT_DIR/.env.dev --env-file $SCRIPT_DIR/.env.secret -v $(pwd):/root/app -w /root/app -p $LOCAL_PORT:$PORT meteofrenchapi:dev $CMD
