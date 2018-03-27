# -*- coding: utf-8 -*-

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
    name = db.Column(db.String(64), unique=False)
    url = db.Column(db.String(64), unique=True)
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
