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

"""repo.py

Repo model.
"""

from datetime import datetime
from .. import db
from . import Subscription


class Repo(db.Model):
    __tablename__ = 'repos'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.Text(), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    github_repo_id = db.Column(db.Integer, unique=True)
    github_webhook_id = db.Column(db.Integer)

    # Associations
    issues = db.relationship('Issue', backref='repo', lazy='dynamic')
    pull_requests = db.relationship(
        'PullRequest', backref='repo', lazy='dynamic'
    )
    subscriptions = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.repo_id],
        backref=db.backref('repo_subscription', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def number_of_cards(self):
        return self.issues.count() + self.pull_requests.count()

    def number_of_issues_by_board_id(self, board_id):
        return len(list(
            filter(lambda x: x.trello_board_id == board_id, self.issues)
        ))

    def number_of_pull_requests_by_board_id(self, board_id):
        return len(list(
            filter(lambda x: x.trello_board_id == board_id, self.pull_requests)
        ))

    def number_of_issues_by_project_key(self, project_key):
        return len(list(
            filter(lambda x: x.jira_project_key == project_key, self.issues)
        ))

    def number_of_pull_requests_by_project_key(self, project_key):
        return len(list(
            filter(lambda x: x.jira_project_key == project_key, self.pull_requests)
        ))

    def number_of_issue_cards(self):
        return len(list(
            filter(lambda x: bool(x.trello_card_id), self.issues)
        ))

    def number_of_pull_request_cards(self):
        return len(list(
            filter(lambda x: bool(x.trello_card_id), self.pull_requests)
        ))

    def number_of_issue_jira_issues(self):
        return len(list(
            filter(lambda x: bool(x.jira_issue_key), self.issues)
        ))

    def number_of_pull_request_jira_issues(self):
        return len(list(
            filter(lambda x: bool(x.jira_issue_key), self.pull_requests)
        ))

    def to_json(self):
        return {
            'label': self.name,
            'value': str(self.github_repo_id)
        }
