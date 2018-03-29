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

"""Change number of characters for issues/prs.

Revision ID: e415dc8c4f46
Revises: d0382d9c12f2
Create Date: 2018-03-29 14:10:57.829813
"""

from alembic import op
import sqlalchemy as sa


revision = 'e415dc8c4f46'
down_revision = 'd0382d9c12f2'


def upgrade():
    op.alter_column(
        'issues', 'name',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'issues', 'url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'pull_requests', 'name',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'pull_requests', 'url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'pull_requests', 'url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'pull_requests', 'name',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'issues', 'url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'issues', 'name',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
