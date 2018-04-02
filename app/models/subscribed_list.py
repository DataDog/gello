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

"""subscribed_list.py

SubscribedList model.
"""

from datetime import datetime
from .. import db


class SubscribedList(db.Model):
    __tablename__ = 'subscribed_lists'

    # Attributes
    subscription_board_id = db.Column(db.String(64), primary_key=True)
    subscription_repo_id = db.Column(db.Integer(), primary_key=True)
    list_id = db.Column(
        db.String(64),
        db.ForeignKey('lists.trello_list_id'),
        primary_key=True
    )
    # The an optional attribute that will assign the trello card created
    trello_member_id = db.Column(db.String(64), unique=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            [subscription_board_id, subscription_repo_id],
            ['subscriptions.board_id', 'subscriptions.repo_id']
        ), {}
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
