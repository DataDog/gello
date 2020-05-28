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

"""subscribed_jira_issue.py

Subscribed JIRA Issues model.
"""

from datetime import datetime
from .. import db


class SubscribedJIRAIssue(db.Model):
    __tablename__ = 'subscribed_jira_issues'

    # Attributes
    subscription_project_key = db.Column(db.String(64), primary_key=True)
    subscription_repo_id = db.Column(db.Integer(), primary_key=True)
    jira_issue_key = db.Column(
        db.String(64),
        db.ForeignKey('jira_parent_issues.jira_issue_key'),
        primary_key=True
    )
    issue_type_name = db.Column(db.String(32), nullable=False)

    # An optional attribute that will assign the created jira issues
    jira_member_id = db.Column(db.String(64), unique=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            [subscription_project_key, subscription_repo_id],
            ['subscriptions.project_key', 'subscriptions.repo_id']
        ), {}
    )
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow)

    # Associations
    parent_issue = db.relationship(
        'JIRAParentIssue',
        backref=db.backref('issue_subscribed_issue', lazy='joined'),
        lazy='joined'
    )
    subscription = db.relationship(
        'Subscription',
        backref=db.backref(
            'subscription_subscribed_jira_issue',
            lazy='joined'
        ),
        lazy='joined'
    )
