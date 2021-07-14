import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8080")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
use_bind = bind_env or f"{host}:{port}"

# Gunicorn config variables
loglevel = use_loglevel
workers = 2
bind = use_bind
keepalive = 120
errorlog = "-"
accesslog = "-"
