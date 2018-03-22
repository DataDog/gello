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

    # Associations
    repo_id = db.Column(db.Integer, db.ForeignKey('repos.id'))

    def to_json(self):
        json_issue = {
            'url': self.url,
            'name': self.name,
            'timestamp': self.timestamp,
        }
        return json_issue

    @staticmethod
    def from_json(json_issue):
        name = json_issue.get('name')
        url = json_issue.get('url')

        return Issue(
            name=name,
            url=url
        )
