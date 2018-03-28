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

"""Add login support

Revision ID: 3b9f644c80e
Revises: 4afcff5d8f0
Create Date: 2018-03-22 12:07:42.148651
"""

from alembic import op
import sqlalchemy as sa


revision = '3b9f644c80e'
down_revision = '4afcff5d8f0'


def upgrade():
    op.add_column(
        'users',
        sa.Column('name', sa.String(length=64), nullable=True)
    )
    op.add_column(
        'users',
        sa.Column('email', sa.String(length=64), nullable=True)
    )
    op.add_column(
        'users',
        sa.Column('password_hash', sa.String(length=128), nullable=True)
    )
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        unique=True
    )


def downgrade():
    op.drop_column('users', 'name')
    op.drop_column('users', 'email')
    op.drop_column('users', 'password_hash')
    op.drop_index('ix_users_email', 'users')
