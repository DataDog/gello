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

"""trello_member.py

TrelloMember model.
"""

from datetime import datetime
from .. import db


class TrelloMember(db.Model):
    __tablename__ = 'trello_members'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=False)
    trello_member_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        return {
            'name': self.name,
            'trello_member_id': self.trello_member_id
        }
