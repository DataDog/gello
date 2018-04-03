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

"""Add username for trello member.

Revision ID: 6f8827878317
Revises: 7ab3b6858963
Create Date: 2018-04-03 11:40:11.319241
"""

from alembic import op
import sqlalchemy as sa


revision = '6f8827878317'
down_revision = '7ab3b6858963'


def upgrade():
    op.add_column(
        'trello_members',
        sa.Column('username', sa.String(length=100), nullable=True)
    )
    op.create_index(
        'ix_trello_members_username',
        'trello_members',
        ['username'],
        unique=True
    )


def downgrade():
    op.drop_column('trello_members', 'username')
    op.drop_index('ix_trello_members_username', 'trello_members')
