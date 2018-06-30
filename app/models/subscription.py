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

"""subscription.py

Subscription model.
"""

from datetime import datetime
from .. import db
from . import SubscribedList


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    # Attributes
    board_id = db.Column(
        db.String(64),
        db.ForeignKey('boards.trello_board_id'),
        primary_key=True
    )
    repo_id = db.Column(
        db.Integer, db.ForeignKey('repos.github_repo_id'), primary_key=True
    )
    issue_autocard = db.Column(db.Boolean, default=True)
    pull_request_autocard = db.Column(db.Boolean, default=True)
    merged_pull_request_autocard = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Associations
    subscribed_lists = db.relationship(
        'SubscribedList',
        foreign_keys=[
            SubscribedList.subscription_board_id,
            SubscribedList.subscription_repo_id
        ],
        backref=db.backref('subscription_subscribed_list', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    board = db.relationship(
        'Board',
        backref=db.backref('subscription_board', lazy='joined'),
        lazy='joined'
    )
    repo = db.relationship(
        'Repo',
        backref=db.backref('subscription_repo', lazy='joined'),
        lazy='joined'
    )
