case $ENV in

  "dev")
    python app.py
    ;;

  "test")
    /bin/sh
    ;;

  "prod" | "staging")
    if [ ! -z $WORKERS ]; then
        args_workers="-w $WORKERS"
    fi
    gunicorn $args_workers app:app
    ;;

  *)
    STATEMENTS
    ;;
esac
