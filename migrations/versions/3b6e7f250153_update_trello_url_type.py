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

"""Update trello_url type.

Revision ID: 3b6e7f250153
Revises: 0afe19626b22
Create Date: 2018-03-30 16:41:29.076091
"""

from alembic import op
import sqlalchemy as sa


revision = '3b6e7f250153'
down_revision = '0afe19626b22'


def upgrade():
    op.alter_column(
        'issues', 'trello_card_url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )
    op.alter_column(
        'pull_requests', 'trello_card_url',
        existing_type=sa.String(length=64),
        type_=sa.Text(),
        existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'pull_requests', 'trello_card_url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
    op.alter_column(
        'issues', 'trello_card_url',
        existing_type=sa.Text(),
        type_=sa.String(length=64),
        existing_nullable=True
    )
