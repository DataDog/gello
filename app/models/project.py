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

"""project.py

JIRA project model.
"""

from datetime import datetime
from .. import db
from . import Subscription
from . import project_issue_types_helper
from . import project_jira_members_helper


class Project(db.Model):
    __tablename__ = 'projects'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    key = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text(), unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations

    parent_issues = db.relationship(
        'JIRAParentIssue',
        backref='project',
        lazy='dynamic'
    )
    issue_types = db.relationship(
        'JIRAIssueType',
        secondary=project_issue_types_helper,
        lazy='dynamic',
        backref=db.backref('projects', lazy=True),
        cascade='all'
    )
    allowed_members = db.relationship(
        'JIRAMember',
        secondary=project_jira_members_helper,
        lazy='dynamic',
        backref=db.backref('projects', lazy=True),
        cascade='all'
    )
    subscription = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.project_key],
        backref=db.backref('project_subscription', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # The jquery UI autocomplete is weird and seems to filter on
    # the label and not the value, so we need to put project keys
    # in as both values here to allow someone to use the project name
    # or project key when searching
    def to_autocomplete(self):
        return {
            'label': self.key,
            'value': self.key
        }

    def to_json(self):
        return {
            'label': self.name,
            'value': self.key
        }
