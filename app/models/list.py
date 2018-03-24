# -*- coding: utf-8 -*-

"""list.py

List model.
"""

from datetime import datetime
from .. import db


class List(db.Model):
    """Based on a Trello list belonging to a particular board."""

    __tablename__ = 'lists'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), unique=False)
    trello_list_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
