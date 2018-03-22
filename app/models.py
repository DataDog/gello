# -*- coding: utf-8 -*-

"""models.py

Models-related logic.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'email': self.email,
            'username': self.username,
            'name': self.name,
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Repo(db.Model):
    __tablename__ = 'repos'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Associations
    issues = db.relationship('Issue', backref='repo', lazy='dynamic')

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
