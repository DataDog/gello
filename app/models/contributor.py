# -*- coding: utf-8 -*-

"""contributor.py

Contributor model.
"""

from datetime import datetime
from .. import db


class Contributor(db.Model):
    __tablename__ = 'contributors'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True)
    member_id = db.Column(db.Integer, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
