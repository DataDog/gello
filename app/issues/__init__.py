# -*- coding: utf-8 -*-

"""__init__.py

issues module initialization code.
"""

from flask import Blueprint

issue = Blueprint('issue', __name__)

from . import views
