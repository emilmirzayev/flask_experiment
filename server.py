import os

from werkzeug.serving import run_simple
from app.factories.app_factory import create_app, SettingsError

if os.environ["settings"]:
    settings_name = os.environ["settings"]
else:
    raise SettingsError("'settings' environment variable is not defined")
app = create_app(__name__, settings_name)


if __name__ == "__main__":
    run_simple(
        "0.0.0.0",5000, application = app, use_reloader=True, use_debugger=app.config["DEBUG"]
    )
