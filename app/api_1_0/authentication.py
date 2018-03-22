# -*- coding: utf-8 -*-

"""authentication.py

Authentication-related API helpers
"""

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from ..models import User
from .errors import unauthorized

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    """"""
    user = User.query.filter_by(email=email).first()

    if not user:
        return False

    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """Errors due to invalid credentials."""
    return unauthorized('Invalid credentials')
