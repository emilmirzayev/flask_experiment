from app.api.choiceset_resource import ChoiceSetResource
from app.api.performance_resource import PerformanceResource
from app.api.event_resource import EventResource
from app.api.recommendation_resource import RecommendationResource
from app.api.answer_resource import AnswerResource
from app.api.question_resource import QuestionResource
from app.api.event_type_resource import EventTypeResource
from app.api.final_set_resource import FinalSetResource

import sys
import logging

from flask import jsonify, Flask

from flask.logging import default_handler

from app.core.extensions import db, ma, migrator


settings = {
    "dev": "app.settings.dev_config.DevelopmentConfig",
    "prod": "core.settings.prod_config.ProductionConfig",
}


class SettingsError(Exception):
    pass


def register_error_handlers(app):
    def create_error_handler(status_code, message):
        def error_handler(error):
            return jsonify(message=message), status_code

        return error_handler

    app.register_error_handler(400, create_error_handler(400, "Bad request"))
    app.register_error_handler(401, create_error_handler(401, "Unathorized"))
    app.register_error_handler(403, create_error_handler(403, "Forbidden"))
    app.register_error_handler(404, create_error_handler(404, "Not found"))


def register_logger(app):
    log_formatter = logging.Formatter(
        "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)
    if app.config["DEBUG"]:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.removeHandler(default_handler)

    return None


def get_config(setting_name):
    if settings.get(setting_name):
        return settings.get(setting_name)
    else:
        raise SettingsError("Given settings name does not exists: %s" % setting_name)


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrator.init_app(app)
    return None


def create_app(app_name, env_name):
    config_obj = get_config(env_name)

    flask_app = Flask(app_name)
    flask_app.config.from_object(config_obj)
    register_logger(flask_app)
    register_extensions(flask_app)
    register_error_handlers(flask_app)
    flask_app.add_url_rule("/events/", view_func=EventResource.as_view("events"))
    flask_app.add_url_rule("/performances/", view_func=PerformanceResource.as_view("performances"))
    flask_app.add_url_rule("/choicesets/", view_func=ChoiceSetResource.as_view("choices"))
    flask_app.add_url_rule("/recommendations/", view_func=RecommendationResource.as_view("recommendations"))
    flask_app.add_url_rule("/answers/", view_func=AnswerResource.as_view("answers"))
    flask_app.add_url_rule("/questions/", view_func=QuestionResource.as_view("questions"))
    flask_app.add_url_rule("/event_types/", view_func=EventTypeResource.as_view("event_types"))
    flask_app.add_url_rule("/final_sets/", view_func=FinalSetResource.as_view("finalsets"))
    
    # flask_app.add_url_rule("/tasks/", view_func=TaskResource.as_view("tasks"))
    flask_app.app_context().push()
    return flask_app
