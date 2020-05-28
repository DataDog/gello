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

"""issue.py

User model.
"""

from datetime import datetime
from .. import db


class Issue(db.Model):
    __tablename__ = 'issues'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    url = db.Column(db.Text(), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    github_issue_id = db.Column(db.Integer, unique=False)
    trello_card_url = db.Column(db.Text(), unique=True)
    trello_card_id = db.Column(db.String(64), unique=True)
    trello_board_id = db.Column(db.String(64), unique=False)
    trello_list_id = db.Column(
        db.String(64), db.ForeignKey('lists.trello_list_id'), unique=False
    )
    jira_issue_key = db.Column(db.String(64), unique=True)
    jira_project_key = db.Column(db.String(64), db.ForeignKey('projects.key'),
                                 unique=False)
    jira_parent_issue_key = db.Column(
        db.String(64),
        db.ForeignKey('jira_parent_issues.jira_issue_key'),
        unique=False
    )

    # Associations
    repo_id = db.Column(db.Integer, db.ForeignKey('repos.github_repo_id'))

    __table_args__ = (db.UniqueConstraint(
        'trello_list_id', 'jira_project_key', 'jira_parent_issue_key',
        'github_issue_id', name='uq_issues_list'),
    )
