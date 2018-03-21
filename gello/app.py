# -*- coding: utf-8 -*-

"""app.py

The main entrypiont for the webserver. Contains routes used by the application.
"""

import json
from gello import settings
from gello.event_receiver import GitHubReceiver
from gello.services import GitHubService
from flask import Flask, request, render_template
from celery import Celery

# Main Flask application
app = Flask(__name__)


class GelloServer(object):
    """Contains routes used by the application."""

    # For processing event actions asynchronously in a task queue
    celery = Celery()

    def __init__(self):
        """Initializes the Flask app and the Celery task queue."""
        self.celery.config_from_object(settings)
        self.github_service = GitHubService()
        app.run(debug=True, use_reloader=True)

    @app.route('/', methods=['GET', 'POST'])
    def index(self):
        """Root url for webserver."""
        if request.method == 'POST':
            # TODO: use a logger
            print("post request from server")

            self.celery.register_task(
                GitHubReceiver(payload=json.loads(request.get_data()))
            )
        elif request.method != 'GET':
            raise ValueError('Unsupported request method type.')

        return render_template('index.html', name='Andrew')

    @app.route('/repos')
    def repos(self):
        """Repos page."""
        return render_template(
            'repos.html',
            organization=self.github_service.organization,
            repo=self.github_service.repos
        )
