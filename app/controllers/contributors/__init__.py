# -*- coding: utf-8 -*-

"""__init__.py

contributor module initialization code.
"""

from flask import Blueprint

contributor = Blueprint('contributor', __name__)

from . import views
