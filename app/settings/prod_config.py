from app.settings.config import Config


class ProdConfig(Config):
    """Configuration class for site production environment"""

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = ""
