# -*- coding: utf-8 -*-

"""pull_request.py

PullRequest model.
"""

from datetime import datetime
from .. import db


class PullRequest(db.Model):
    __tablename__ = 'pull_requests'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    repo_id = db.Column(db.Integer, db.ForeignKey('repos.id'))
