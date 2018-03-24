# -*- coding: utf-8 -*-

"""board.py

Board model.
"""

from datetime import datetime
from .. import db


class Board(db.Model):
    __tablename__ = 'boards'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    trello_board_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    repos = db.relationship('Repo', backref='board', lazy='dynamic')
    lists = db.relationship('List', backref='board', lazy='dynamic')
