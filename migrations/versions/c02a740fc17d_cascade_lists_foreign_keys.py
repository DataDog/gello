
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade lists foreign keys

Revision ID: c02a740fc17d
Revises: 5fee1f45c95b
Create Date: 2022-11-28 20:32:48.403470
"""

from alembic import op
import sqlalchemy as sa


revision = 'c02a740fc17d'
down_revision = '5fee1f45c95b'


def upgrade():
    op.drop_constraint(constraint_name="lists_board_id_fkey", table_name="lists", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="lists_board_id_fkey",
        source_table="lists",
        referent_table="boards",
        local_cols=["board_id"],
        remote_cols=["trello_board_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="lists_board_id_fkey", table_name="lists", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="lists_board_id_fkey",
        source_table="lists",
        referent_table="boards",
        local_cols=["board_id"],
        remote_cols=["trello_board_id"]
    )

    pass
