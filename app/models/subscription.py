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
from . import SubscribedJIRAIssue
from . import SubscribedJIRAProject


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    # Attributes
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    board_id = db.Column(
        db.String(64),
        db.ForeignKey('boards.trello_board_id'),
        unique=True
    )
    repo_id = db.Column(
        db.Integer, db.ForeignKey('repos.github_repo_id'), primary_key=True
    )
    project_key = db.Column(
        db.String(64),
        db.ForeignKey('projects.key')
    )
    issue_autocard = db.Column(db.Boolean, default=True)
    pull_request_autocard = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            'project_key', 'repo_id', name='subscriptions_project_key_key'
        ),
        db.UniqueConstraint(
            'board_id', 'repo_id', name='subscriptions_board_id_key'
        ),
    )

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
    subscribed_jira_issues = db.relationship(
        'SubscribedJIRAIssue',
        foreign_keys=[
            SubscribedJIRAIssue.subscription_project_key,
            SubscribedJIRAIssue.subscription_repo_id
        ],
        backref=db.backref(
            'subscription_subscribed_jira_issue',
            lazy='joined'
        ),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    subscribed_jira_projects = db.relationship(
        'SubscribedJIRAProject',
        foreign_keys=[
            SubscribedJIRAProject.subscription_project_key,
            SubscribedJIRAProject.subscription_repo_id
        ],
        backref=db.backref(
            'subscription_subscribed_jira_project',
            lazy='joined'
        ),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    board = db.relationship(
        'Board',
        backref=db.backref('subscription_board', lazy='joined'),
        lazy='joined'
    )
    project = db.relationship(
        'Project',
        backref=db.backref('subscription_project', lazy='joined'),
        lazy='joined'
    )
    repo = db.relationship(
        'Repo',
        backref=db.backref('subscription_repo', lazy='joined'),
        lazy='joined'
    )
