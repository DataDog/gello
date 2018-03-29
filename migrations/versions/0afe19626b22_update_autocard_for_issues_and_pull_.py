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

"""Update autocard for issues and pull requests.

Revision ID: 0afe19626b22
Revises: 1bcac2a750c2
Create Date: 2018-03-30 15:45:38.643314
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


revision = '0afe19626b22'
down_revision = '1bcac2a750c2'

Session = sessionmaker()
Base = declarative_base()


class Repo(Base):
    """Repo class 'partial' state at point of migration."""
    __tablename__ = 'repos'

    # Required attributes
    id = sa.Column(sa.Integer, primary_key=True)
    github_repo_id = sa.Column(sa.Integer, unique=True)


class Board(Base):
    """Board class 'partial' state at point of migration."""
    __tablename__ = 'boards'

    # Required attributes
    id = sa.Column(sa.Integer, primary_key=True)
    trello_board_id = sa.Column(sa.String(64), unique=True)


class Subscription(Base):
    """Subscription class 'partial' state at point of migration."""
    __tablename__ = 'subscriptions'

    # Attributes
    board_id = sa.Column(
        sa.String(64),
        sa.ForeignKey('boards.trello_board_id'),
        primary_key=True
    )
    repo_id = sa.Column(
        sa.Integer, sa.ForeignKey('repos.github_repo_id'), primary_key=True
    )
    issue_autocard = sa.Column(sa.Boolean, default=True)
    pull_request_autocard = sa.Column(sa.Boolean, default=True)


def upgrade():
    """For each autocard subscription, make the pull_request_aucocard True."""
    bind = op.get_bind()
    session = Session(bind=bind)

    op.alter_column(
        'subscriptions', 'autocard',
        new_column_name='issue_autocard'
    )
    op.add_column(
        'subscriptions',
        sa.Column(
            'pull_request_autocard',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )

    for sub in session.query(Subscription).filter_by(issue_autocard=True):
        sub.pull_request_autocard = True

    session.commit()


def downgrade():
    """Downgrade to previous state with only one `autocard` value."""
    op.drop_column('subscriptions', 'pull_request_autocard')
    op.alter_column(
        'subscriptions', 'issue_autocard',
        new_column_name='autocard'
    )
