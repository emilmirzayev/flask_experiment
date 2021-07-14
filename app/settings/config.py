import os

from flask_env import MetaFlaskEnv


class Config(metaclass=MetaFlaskEnv):
    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """

    DEBUG = True
    ASSETS_DEBUG = False  # not DEBUG
    CSRF_ENABLED = True

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
