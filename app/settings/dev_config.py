from app.settings.config import Config


class DevelopmentConfig(Config):
    """Configuration class for site development environment"""

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/test.db"
