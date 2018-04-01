# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

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
    name = db.Column(db.Text(), unique=True)
    url = db.Column(db.Text(), unique=True)
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

    def to_json(self):
        return {
            'trello_board_id': self.trello_board_id,
            'name': self.name,
            'url': self.url
        }
