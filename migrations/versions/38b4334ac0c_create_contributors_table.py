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

"""Create contributors table

Revision ID: 38b4334ac0c
Revises: 52460a6cc39
Create Date: 2018-03-23 09:58:28.383941
"""

from alembic import op
import sqlalchemy as sa


revision = '38b4334ac0c'
down_revision = '52460a6cc39'


def upgrade():
    op.create_table(
        'contributors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(length=64), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_contributors_member_id',
        'contributors',
        ['member_id'],
        unique=True
    )


def downgrade():
    op.drop_index('ix_contributors_member_id', 'contributors')
    op.drop_table('contributors')
