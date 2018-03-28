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

"""Create boards table

Revision ID: 57bc1ebd1cc
Revises: 38b4334ac0c
Create Date: 2018-03-23 14:13:34.382572
"""

from alembic import op
import sqlalchemy as sa


revision = '57bc1ebd1cc'
down_revision = '38b4334ac0c'


def upgrade():
    op.create_table(
        'boards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('url', sa.String(length=64), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_boards_timestamp', 'boards', ['timestamp'], unique=False
    )
    op.add_column(
        'repos',
        sa.Column('board_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_repos_board_id_boards',
        'repos', 'boards',
        ['board_id'], ['id'],
    )


def downgrade():
    op.drop_column('repos', 'board_id')
    op.drop_index('ix_boards_timestamp', 'boards')
    op.drop_table('boards')
