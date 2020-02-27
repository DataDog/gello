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

"""jira_issue_types.py

JIRA issue types model.
"""

from datetime import datetime
from .. import db
# import project


class JIRAIssueTypes(db.Model):
    __tablename__ = 'jira_issue_types'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    url = db.Column(db.Text(), unique=True)
    description = db.Column(db.Text(), unique=False)
    issue_type_id = db.Column(db.String(64), unique=True)
    subtask = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    # is associated with jira projects via backref 'projects'

    def to_json(self):
        return {
            'label': self.name,
            'value': self.issue_type_id
        }
