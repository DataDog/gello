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

"""list.py

List model.
"""

from datetime import datetime
from .. import db
from . import SubscribedList


class List(db.Model):
    """Based on a Trello list belonging to a particular board."""

    __tablename__ = 'lists'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    trello_list_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    board_id = db.Column(
        db.String(64), db.ForeignKey('boards.trello_board_id')
    )
    subscribed_lists = db.relationship(
        'SubscribedList',
        foreign_keys=[SubscribedList.list_id],
        backref=db.backref('list_subscribed_list', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
