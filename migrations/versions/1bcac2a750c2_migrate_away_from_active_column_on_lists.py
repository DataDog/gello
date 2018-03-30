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

"""Migrate away from 'active' column on lists.

Revision ID: 1bcac2a750c2
Revises: 4556966b899e
Create Date: 2018-03-30 13:45:13.205907
"""

import sqlalchemy as sa
from alembic import op
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


revision = '1bcac2a750c2'
down_revision = '4556966b899e'

Session = sessionmaker()
Base = declarative_base()


class Board(Base):
    """Board class state at point of migration."""
    __tablename__ = 'boards'

    # Attributes
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text(), unique=True)
    url = sa.Column(sa.Text(), unique=True)
    trello_board_id = sa.Column(sa.String(64), unique=True)
    timestamp = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)


class SubscribedList(Base):
    """SubscribedList class state at point of migration."""
    __tablename__ = 'subscribed_lists'

    # Attributes
    subscription_board_id = sa.Column(sa.String(64), primary_key=True)
    subscription_repo_id = sa.Column(sa.Integer(), primary_key=True)
    list_id = sa.Column(
        sa.String(64),
        sa.ForeignKey('lists.trello_list_id'),
        primary_key=True
    )
    __table_args__ = (
        sa.ForeignKeyConstraint(
            [subscription_board_id, subscription_repo_id],
            ['subscriptions.board_id', 'subscriptions.repo_id']
        ), {}
    )
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)


class Subscription(Base):
    """Subscription class state at point of migration."""
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
    autocard = sa.Column(sa.Boolean, default=True)
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)


class List(Base):
    """List class state at point of migration."""
    __tablename__ = 'lists'

    # Attributes
    id = sa.Column(sa.Integer, primary_key=True)
    active = sa.Column(sa.Boolean, default=False)
    name = sa.Column(sa.String(64), unique=False)
    trello_list_id = sa.Column(sa.String(64), unique=True)
    timestamp = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)

    # Associations
    board_id = sa.Column(
        sa.String(64), sa.ForeignKey('boards.trello_board_id')
    )


def upgrade():
    """Create the new subscribed lists from the active ones."""
    bind = op.get_bind()
    session = Session(bind=bind)

    for subscription in session.query(Subscription):
        # Iterate through all the active lists for a given board
        for trello_list in session.query(List).filter_by(
                active=True, board_id=subscription.board_id):
            record = session.query(SubscribedList).filter_by(
                subscription_board_id=subscription.board_id,
                subscription_repo_id=subscription.repo_id,
                list_id=trello_list.trello_list_id
            ).first()

            # Safety check
            if not record:
                subscribed_list = SubscribedList(
                    subscription_board_id=subscription.board_id,
                    subscription_repo_id=subscription.repo_id,
                    list_id=trello_list.trello_list_id
                )
                session.add(subscribed_list)

    session.commit()

    # Remove `active`
    op.drop_column('lists', 'active')


def downgrade():
    """Reverts the database back to the old `active` format."""
    bind = op.get_bind()
    session = Session(bind=bind)

    op.add_column(
        'lists',
        sa.Column(
            'active', sa.Boolean(), nullable=False, server_default='false'
        )
    )

    for subscribed_list in session.query(SubscribedList):
        trello_list = session.query(List).filter_by(
            trello_list_id=subscribed_list.list_id
        ).first()
        trello_list.active = True

    session.commit()
