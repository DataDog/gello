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

"""Add trello_board_id to Board model.

Revision ID: 240c1be6b0d
Revises: 57bc1ebd1cc
Create Date: 2018-03-24 13:26:48.326446
"""

from alembic import op
import sqlalchemy as sa


revision = '240c1be6b0d'
down_revision = '57bc1ebd1cc'


def upgrade():
    op.add_column(
        'boards',
        sa.Column('trello_board_id', sa.String(length=64), nullable=False)
    )
    op.create_index(
        'ix_boards_trello_board_id', 'boards', ['trello_board_id'], unique=True
    )


def downgrade():
    op.drop_index('ix_boards_trello_board_id', 'boards')
    op.drop_column('boards', 'trello_board_id')
