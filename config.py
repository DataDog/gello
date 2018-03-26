# -*- coding: utf-8 -*-

"""config.py

Configuration for the Flask application.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BROKER_POOL_LIMIT = 0
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or \
        'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or \
        'redis://localhost:6379/0'
    DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
    GITHUB_ORG_LOGIN = os.environ.get('GITHUB_ORG_LOGIN')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bad_secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuration for testing production."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @classmethod
    def init_app(cls, app):
        """Initializes production application."""
        Config.init_app(app)


class HerokuConfig(ProductionConfig):
    """Configuration for Heroku."""
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        """Initializes Heroku application."""
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
