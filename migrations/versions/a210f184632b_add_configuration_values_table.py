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

"""Add configuration values table.

Revision ID: a210f184632b
Revises: bde502a0cc6f
Create Date: 2018-04-27 13:39:41.433077
"""

from alembic import op
import sqlalchemy as sa


revision = 'a210f184632b'
down_revision = 'bde502a0cc6f'


def upgrade():
    op.create_table(
        'config_values',
        sa.Column('key', sa.Text(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('key')
    )


def downgrade():
    op.drop_table('config_values')
