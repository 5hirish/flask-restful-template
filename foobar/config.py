import os
from env_loader import load_env_config


class Config:
    """Base configuration."""

    load_env_config()

    if str(os.environ.get('FLASK_ENV')) != 'prod':
        app_debug = True
    else:
        app_debug = False

    # ------- Flask Config --------

    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_NAME = 'foobar_app'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    BROKER_POOL_LIMIT = 1

    FILE_STREAM_LIMIT = 53687091200     # 50 Gigabytes

    # ------- Database Uris --------

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # ------- Credentials Config --------

    AWS_S3_PRODUCT_BUCKET = os.getenv("AWS_S3_PRODUCT_BUCKET")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


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

    CELERY_TASK_ALWAYS_EAGER = True


def get_config(env_type=None):
    if env_type is None:
        env_type = os.getenv('FLASK_APP')

    if env_type == 'test':
        return TestConfig
    elif env_type == 'prod':
        return ProdConfig
    else:
        return DevConfig

