#! /bin/bash
set -e

DEFAULT_MODULE_NAME=server

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

DEFAULT_GUNICORN_CONF=./gunicorn_conf.py

export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export FLASK_APP=$APP_MODULE
# Run migrations
SQLITE_DB_FILE=./db/test.db
if [ -f "$SQLITE_DB_FILE" ]; then
    echo "$SQLITE_DB_FILE exists. Skipping [flask db init] command"
else
    flask db init
fi
flask db migrate -m "migration message"
flask db upgrade


# Start Gunicorn
gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"