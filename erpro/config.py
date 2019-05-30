import os
from dotenv import load_dotenv


class Config:
    """Base configuration."""

    if str(os.environ.get('FLASK_ENV')) != 'prod':
        app_debug = True
        load_dotenv(verbose=True)
    else:
        app_debug = False

    STATIC_FILE_PATH = os.path.join(os.getcwd(), 'static')

    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_NAME = 'erpro_app'

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    # BROKER_POOL_LIMIT = 1


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True

    SQLALCHEMY_ECHO = True

    SESSION_COOKIE_SECURE = False

    SENTRY_DSN = ""


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'
    TESTING = True
    DEBUG = True



