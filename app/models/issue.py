# -*- coding: utf-8 -*-

"""issue.py

User model.
"""

from datetime import datetime
from .. import db


class Issue(db.Model):
    __tablename__ = 'issues'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    github_issue_id = db.Column(db.Integer, unique=True)

    # Associations
    repo_id = db.Column(db.Integer, db.ForeignKey('repos.id'))
