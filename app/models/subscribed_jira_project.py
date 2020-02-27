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

"""subscribed_jira_project.py

Subscribed JIRA Projects model.
"""

from datetime import datetime
from .. import db


class SubscribedJIRAProject(db.Model):
    __tablename__ = 'subscribed_jira_projects'

    # Attributes
    subscription_repo_id = db.Column(db.Integer(), primary_key=True)
    subscription_project_key = db.Column(
        db.String(64),
        primary_key=True
    )
    issue_type_id = db.Column(
        db.String(64),
        db.ForeignKey('jira_issue_types.issue_type_id')
    )

    # An optional attribute that will assign the trello card created
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
    subscription = db.relationship(
        'Subscription',
        backref=db.backref('subscription_subscribed_jira_project', lazy='joined'),
        lazy='joined'
    )
