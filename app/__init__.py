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

"""__init__.py

Create a modular flask application with database.
"""

import os
from flask import Flask, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from celery import Celery

# load environment variable for local development/ migration
if os.path.exists('.env'):
    print('Importing environment from .env in __init__...')

    from dotenv import load_dotenv
    load_dotenv()

from config import config, Config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """Initializes a modular flask application:

        - Initializes all the Flask extensions
        - Configures Celery Task queue
        - Hooks up all the blueprints
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    celery.conf.update(app.config)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .controllers.onboarding import onboarding as onboarding_blueprint
    app.register_blueprint(onboarding_blueprint, url_prefix='/onboarding')

    from .controllers.repos import repo as repo_blueprint
    app.register_blueprint(repo_blueprint, url_prefix='/repos')

    from .controllers.issues import issue as issue_blueprint
    app.register_blueprint(issue_blueprint, url_prefix='/repos/issues')

    from .controllers.boards import board as board_blueprint
    app.register_blueprint(board_blueprint, url_prefix='/boards')

    from .controllers.pull_requests import pull_request as pr_blueprint
    app.register_blueprint(pr_blueprint, url_prefix='/repos/pull_requests')

    from .controllers.github_members import github_member as \
        github_member_blueprint
    app.register_blueprint(github_member_blueprint, url_prefix='/github_members')

    from .controllers.trello_members import trello_member as \
        trello_member_blueprint
    app.register_blueprint(trello_member_blueprint, url_prefix='/trello_members')

    from .controllers.trello_lists import trello_list as trello_list_blueprint
    app.register_blueprint(trello_list_blueprint, url_prefix='/boards/lists')

    from .controllers.subscribed_lists import subscribed_list as \
        subscribed_list_blueprint
    app.register_blueprint(subscribed_list_blueprint, url_prefix='/subscriptions/lists')

    from .controllers.subscriptions import subscription as subscription_blueprint
    app.register_blueprint(subscription_blueprint, url_prefix='/subscriptions')

    return app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.before_request
def before_request():
    """
    If not all the required environment variables are set, and not viewing an
    onboarding route redirect to the onboarding view.
    """
    if current_user.is_authenticated:
        # Don't redirect to the `/onboarding` route for these routes
        if request.endpoint.startswith('api') or \
           request.endpoint.startswith('auth'):
            return

        if ('TRELLO_ORG_NAME' not in os.environ or 'GITHUB_ORG_LOGIN' not in
           os.environ) and not request.endpoint.startswith('onboarding'):
            return redirect(url_for('onboarding.index'))
        elif ('TRELLO_ORG_NAME' in os.environ and 'GITHUB_ORG_LOGIN' in
              os.environ) and request.endpoint.startswith('onboarding'):
            return redirect(url_for('main.index'))


# Configure tracing if `APM_ENABLED` is `True`
if app.config.get('APM_ENABLED'):
    from ddtrace import tracer, patch
    from ddtrace.contrib.flask import TraceMiddleware

    # Required for Flask middleware:
    #   http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask
    import blinker as _

    patch(celery=True)
    patch(sqlalchemy=True)

    traced_app = TraceMiddleware(
        app,
        tracer,
        service='gello',
        distributed_tracing=False
    )
