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
    name = db.Column(db.String(100), unique=False)
    url = db.Column(db.Text(), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    github_repo_id = db.Column(db.Integer, unique=True)

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
