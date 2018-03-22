#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""celery_worker.py

A celery worker to be run in a separate process by:

    `celery worker -A celery_worker.celery --loglevel=info`
"""

import os

# The celery import is required for proper configuration of the server. Flake8
# will complain it's not being used, but don't delete this
from app import celery, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
