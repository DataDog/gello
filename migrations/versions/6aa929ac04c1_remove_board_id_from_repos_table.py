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

"""Remove board_id from repos table.

Revision ID: 6aa929ac04c1
Revises: 5dc3ef40c98c
Create Date: 2018-03-26 19:53:12.589522
"""

from alembic import op
import sqlalchemy as sa


revision = '6aa929ac04c1'
down_revision = '5dc3ef40c98c'


def upgrade():
    op.drop_index('ix_boards_timestamp', 'boards')
    op.drop_column('repos', 'board_id')


def downgrade():
    op.add_column(
        'repos',
        sa.Column('board_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_repos_board_id_boards',
        'repos', 'boards',
        ['board_id'], ['id'],
    )
