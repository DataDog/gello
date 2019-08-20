# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""config.py

Configuration for the Flask application.
"""

import os
from flask_dotenv import DotEnv


class Config:
    APM_ENABLED = 'APM_ENABLED' in os.environ
    BROKER_POOL_LIMIT = 0
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or \
        'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or \
        'redis://localhost:6379/0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bad_secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_DISABLE = False

    REPO_LABELS = {
        'dd-trace-go': 'Go',
        'dd-trace-php': 'PHP',
        'dd-trace-py': 'Python',
        'dd-trace-rb': 'Ruby',
        'dd-trace-java': 'Java',
        'dd-trace-js': 'Javascript',
        'dd-trace-dotnet': '.Net'
    }

    @staticmethod
    def init_app(app):
        env_file_path = os.path.join(app.root_path, '../', '.env')

        if os.path.exists(env_file_path):
            env = DotEnv()
            env.init_app(app)


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Configuration for testing environment."""
    CELERY_ALWAYS_EAGER = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
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
