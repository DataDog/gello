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

"""create configuration table

Revision ID: bb8492da24f1
Revises: 27f4371eff83
Create Date: 2019-08-01 10:07:33.663740
"""

from alembic import op
import sqlalchemy as sa


revision = 'bb8492da24f1'
down_revision = '27f4371eff83'


def upgrade():
    """Creates a simple key value table for non-sensitive environment info.
    """
    op.create_table(
        'config_values',
        sa.Column('key', sa.Text(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('key')
    )


def downgrade():
    op.drop_table('config_values')
