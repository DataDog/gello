# -*- coding: utf-8 -*-

"""repo.py

Repo model.
"""

from datetime import datetime
from .. import db


class Repo(db.Model):
    __tablename__ = 'repos'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    issues = db.relationship('Issue', backref='repo', lazy='dynamic')
    pull_requests = db.relationship('PullRequest', backref='repo', lazy='dynamic')

    def to_json(self):
        json_repo = {
            'url': self.url,
            'name': self.name,
            'timestamp': self.timestamp,
            # 'issues': url_for('api.get_repo_issues', id=self.id, _external=True),
        }
        return json_repo

    @staticmethod
    def from_json(json_repo):
        name = json_repo.get('name')
        url = json_repo.get('url')

        return Repo(
            name=name,
            url=url
        )
