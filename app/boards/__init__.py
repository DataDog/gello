# -*- coding: utf-8 -*-

"""__init__.py

repos module initialization code.
"""

from flask import Blueprint

board = Blueprint('board', __name__)

from . import views
