# -*- coding: utf-8 -*-

"""__init__.py

subscriptions module initialization code.
"""

from flask import Blueprint

subscription = Blueprint('subscription', __name__)

from . import views
