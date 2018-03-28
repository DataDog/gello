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

"""Add trello card details to the Issue and PullRequest models.

Revision ID: 4ad18f16a937
Revises: 2b5eb14b042e
Create Date: 2018-03-28 14:46:00.704598
"""

from alembic import op
import sqlalchemy as sa


revision = '4ad18f16a937'
down_revision = '2b5eb14b042e'


def upgrade():
    op.add_column(
        'pull_requests',
        sa.Column('trello_card_url', sa.String(length=64), nullable=True)
    )
    op.add_column(
        'pull_requests',
        sa.Column('trello_card_id', sa.String(length=64), nullable=True)
    )
    op.create_index(
        'ix_pull_requests_trello_card_id',
        'pull_requests',
        ['trello_card_id'],
        unique=True
    )

    op.add_column(
        'issues',
        sa.Column('trello_card_url', sa.String(length=64), nullable=True)
    )
    op.add_column(
        'issues',
        sa.Column('trello_card_id', sa.String(length=64), nullable=True)
    )
    op.create_index(
        'ix_issues_trello_card_id',
        'issues',
        ['trello_card_id'],
        unique=True
    )


def downgrade():
    # Issues
    op.drop_index('ix_issues_trello_card_id', 'issues')
    op.drop_column('issues', 'trello_card_id')
    op.drop_column('issues', 'trello_card_url')

    # Pull Requests
    op.drop_index('ix_pull_requests_trello_card_id', 'pull_requests')
    op.drop_column('pull_requests', 'trello_card_id')
    op.drop_column('pull_requests', 'trello_card_url')
