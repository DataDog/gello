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

"""Add trello_members table.

Revision ID: b33ff8ffcacc
Revises: 017e7b4c7a98
Create Date: 2018-04-02 10:47:15.912064
"""

from alembic import op
import sqlalchemy as sa


revision = 'b33ff8ffcacc'
down_revision = '017e7b4c7a98'


def upgrade():
    op.create_table(
        'trello_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('trello_member_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_trello_members_member_id',
        'trello_members',
        ['trello_member_id'],
        unique=True
    )


def downgrade():
    op.drop_index('ix_trello_members_member_id', 'trello_members')
    op.drop_table('trello_members')
