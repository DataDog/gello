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
from . import SubscribedJIRAProject


class Project(db.Model):
    __tablename__ = 'projects'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    url = db.Column(db.Text(), unique=True)
    key = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text(), unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

# TODO?: associations including subscription, issues, and issue types

    # # Associations

    parent_issues = db.relationship(
        'JIRAParentIssue',
        backref='project',
        lazy='dynamic'
    )
    issue_types = db.relationship(
        'JIRAIssueTypes',
        secondary=project_issue_types_helper,
        lazy=True,
        backref=db.backref('projects', lazy=True)
    )
    subscription = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.project_key],
        backref=db.backref('project_subscription', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def to_json(self):
        return {
            'label': self.name,
            'value': self.key
        }
