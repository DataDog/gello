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

"""Change number of characters for columns.

Revision ID: d0382d9c12f2
Revises: 4ad18f16a937
Create Date: 2018-03-29 13:59:57.094872
"""

from alembic import op
import sqlalchemy as sa


revision = 'd0382d9c12f2'
down_revision = '4ad18f16a937'


def upgrade():
    op.alter_column(
        'repos', 'name',
        existing_type=sa.String(length=64),
        type_=sa.String(length=100),
        existing_nullable=True
    )
    op.alter_column(
        'repos', 'url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'boards', 'name',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'boards', 'url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'boards', 'url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'boards', 'name',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'repos', 'url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'repos', 'name',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=64),
        existing_nullable=True
    )
