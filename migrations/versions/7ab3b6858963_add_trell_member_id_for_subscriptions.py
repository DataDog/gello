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

"""Add trello_member_id for subscriptions.

Revision ID: 7ab3b6858963
Revises: b33ff8ffcacc
Create Date: 2018-04-02 11:54:41.793914
"""

from alembic import op
import sqlalchemy as sa


revision = '7ab3b6858963'
down_revision = 'b33ff8ffcacc'


def upgrade():
    op.add_column(
        'subscribed_lists',
        sa.Column('trello_member_id', sa.String(length=64), nullable=True)
    )


def downgrade():
    op.drop_column('subscribed_lists', 'trello_member_id')
