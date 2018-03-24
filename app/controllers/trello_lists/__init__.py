# -*- coding: utf-8 -*-

"""__init__.py

issues module initialization code.
"""

from flask import Blueprint

trello_list = Blueprint('trello_list', __name__)

from . import views
