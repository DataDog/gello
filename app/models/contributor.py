# -*- coding: utf-8 -*-

"""contributor.py

Contributor model.
"""

from datetime import datetime
from .. import db


class Contributor(db.Model):
    __tablename__ = 'contributors'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True)
    member_id = db.Column(db.Integer, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        json_contributor = {
            'login': self.login,
            'member_id': self.member_id,
            'timestamp': self.timestamp,
        }
        return json_contributor

    @staticmethod
    def from_json(json_contributor):
        login = json_contributor.get('login')
        member_id = json_contributor.get('member_id')

        return Contributor(
            login=login,
            member_id=member_id
        )
