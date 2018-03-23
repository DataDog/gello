# -*- coding: utf-8 -*-

"""main/views.py

repos-related routes and view-specific logic.
"""

from flask import render_template, current_app

from . import main
from ...tasks import GitHubReceiver


@main.route('/', methods=['GET', 'POST'])
def index():
    GitHubReceiver.delay({"issue": "test"})
    return render_template('index.html')
