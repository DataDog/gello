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

"""Create users table

Revision ID: 4afcff5d8f0
Revises: None
Create Date: 2018-03-22 12:05:31.690991
"""

from alembic import op
import sqlalchemy as sa


revision = '4afcff5d8f0'
down_revision = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)


def downgrade():
    op.drop_index('ix_users_username', 'users')
    op.drop_table('users')
