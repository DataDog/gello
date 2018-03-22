# -*- coding: utf-8 -*-

"""main/views.py

repos-related routes and view-specific logic.
"""

from flask import render_template, current_app

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
