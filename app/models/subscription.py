# -*- coding: utf-8 -*-

"""subscription.py

Subscription model.
"""

from datetime import datetime
from .. import db


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    # Attributes
    board_id = db.Column(
        db.Integer, db.ForeignKey('boards.id'), primary_key=True
    )
    repo_id = db.Column(
        db.Integer, db.ForeignKey('repos.id'), primary_key=True
    )
    autocard = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
