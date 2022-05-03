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
python3 -m flask db migrate -m "initial migrate"
python3 -m flask db upgrade


# Start Gunicorn
python3 -m gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"