# -*- coding: utf-8 -*-

"""board.py

Board model.
"""

from datetime import datetime
from .. import db
from . import Subscription


class Board(db.Model):
    __tablename__ = 'boards'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    trello_board_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    lists = db.relationship('List', backref='board', lazy='dynamic')
    subscription = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.board_id],
        backref=db.backref('board_subscription', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
