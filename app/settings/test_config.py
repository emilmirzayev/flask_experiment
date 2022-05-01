from app.settings.config import Config


class TestConfig(Config):
    """Configuration class for site production environment"""

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/test2.db"
