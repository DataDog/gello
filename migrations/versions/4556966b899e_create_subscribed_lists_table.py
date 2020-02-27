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

"""Create subscribed_lists table.

Revision ID: 4556966b899e
Revises: e415dc8c4f46
Create Date: 2018-03-30 10:17:45.307946
"""

from alembic import op
import sqlalchemy as sa


revision = '4556966b899e'
down_revision = 'e415dc8c4f46'


def upgrade():
    op.create_table(
        'subscribed_lists',
        sa.Column('subscription_board_id', sa.String(64), nullable=False),
        sa.Column('subscription_repo_id', sa.Integer(), nullable=False),
        sa.Column('list_id', sa.String(64), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['subscription_board_id', 'subscription_repo_id'],
            ['subscriptions.board_id', 'subscriptions.repo_id'],
            name='subscribed_lists_subscription_board_id_subscription_repo_i_fkey'
        ),
        sa.ForeignKeyConstraint(['list_id'], ['lists.trello_list_id']),
        sa.PrimaryKeyConstraint(
            'subscription_board_id', 'subscription_repo_id', 'list_id'
        )
    )


def downgrade():
    op.drop_table('subscribed_lists')
