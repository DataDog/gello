# -*- coding: utf-8 -*-

"""__init__.py

pull_requests module initialization code.
"""

from flask import Blueprint

pull_request = Blueprint('pull_request', __name__)

from . import views
