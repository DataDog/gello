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

"""Add trello_board_id to card objects Issue and PullRequest

Revision ID: 97c9100c8b46
Revises: 6f8827878317
Create Date: 2018-04-04 10:48:26.691464
"""

from alembic import op
import sqlalchemy as sa


revision = '97c9100c8b46'
down_revision = '6f8827878317'


def upgrade():
    op.add_column(
        'issues',
        sa.Column('trello_board_id', sa.String(64), nullable=True)
    )
    op.add_column(
        'pull_requests',
        sa.Column('trello_board_id', sa.String(64), nullable=True)
    )


def downgrade():
    op.drop_column('issues', 'trello_board_id')
    op.drop_column('pull_requests', 'trello_board_id')
