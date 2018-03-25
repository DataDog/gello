# -*- coding: utf-8 -*-

"""main/views.py

repos-related routes and view-specific logic.
"""

import json
from flask import render_template, current_app, request
from . import main
from ...tasks import GitHubReceiver


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        GitHubReceiver.delay(payload=json.loads(request.get_data()))
        return "GitHub event received."

    return render_template('index.html')
