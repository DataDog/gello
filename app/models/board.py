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
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    repos = db.relationship('Repo', backref='board', lazy='dynamic')

    def to_json(self):
        json_board = {
            'url': self.url,
            'name': self.name,
            'timestamp': self.timestamp,
        }
        return json_board

    @staticmethod
    def from_json(json_board):
        name = json_board.get('name')
        url = json_board.get('url')

        return Board(
            name=name,
            url=url
        )
