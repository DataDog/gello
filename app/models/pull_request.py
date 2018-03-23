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

    def to_json(self):
        json_pull_request = {
            'url': self.url,
            'name': self.name,
            'timestamp': self.timestamp,
        }
        return json_pull_request

    @staticmethod
    def from_json(json_pull_request):
        name = json_pull_request.get('name')
        url = json_pull_request.get('url')

        return PullRequest(
            name=name,
            url=url
        )
