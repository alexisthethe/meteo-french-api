case $ENV in

  "dev")
    python app.py
    ;;

  "test")
    /bin/sh
    ;;

  "prod" | "staging")
    if [ ! -z $GUNICORN_WORKERS ]; then
        args_workers="-w $GUNICORN_WORKERS"
    fi
    gunicorn $args_workers app:app -b 0.0.0.0:$PORT
    ;;

  *)
    echo "environment variable ENV=$ENV unknown"
    ;;
esac
