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

"""jira_member.py

JIRAMember model.
"""

from datetime import datetime
from .. import db


class JIRAMember(db.Model):
    __tablename__ = 'jira_members'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Text(), unique=False)
    email = db.Column(db.String(100), unique=True)
    jira_account_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        return {
            'label': self.email,
            'value': self.jira_member_id
        }
