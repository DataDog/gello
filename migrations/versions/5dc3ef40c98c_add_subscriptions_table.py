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

"""Add subscriptions table.

Revision ID: 5dc3ef40c98c
Revises: 56d8a1d3682
Create Date: 2018-03-26 10:15:16.315747
"""

from alembic import op
import sqlalchemy as sa


revision = '5dc3ef40c98c'
down_revision = '56d8a1d3682'


def upgrade():
    op.create_table(
        'subscriptions',
        sa.Column('board_id', sa.String(length=64), nullable=False),
        sa.Column('repo_id', sa.Integer(), nullable=False),
        sa.Column('autocard', sa.Boolean(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['board_id'], ['boards.trello_board_id']),
        sa.ForeignKeyConstraint(['repo_id'], ['repos.github_repo_id']),
        sa.PrimaryKeyConstraint('board_id', 'repo_id')
    )


def downgrade():
    op.drop_table('subscriptions')
