
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade subscribed_lists foreign keys

Revision ID: 8ef81fc51dc0
Revises: 1dfef2c5de0f
Create Date: 2022-11-29 21:46:31.308802
"""

from alembic import op
import sqlalchemy as sa


revision = '8ef81fc51dc0'
down_revision = '1dfef2c5de0f'


def upgrade():
    op.drop_constraint(constraint_name="subscribed_lists_list_id_fkey", table_name="subscribed_lists", type_="foreignkey")
    op.drop_constraint(constraint_name="subscribed_lists_subscription_board_id_fkey", table_name="subscribed_lists", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_lists_list_id_fkey",
        source_table="subscribed_lists",
        referent_table="lists",
        local_cols=["list_id"],
        remote_cols=["trello_list_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="subscribed_lists_subscription_board_id_fkey",
        source_table="subscribed_lists",
        referent_table="subscriptions",
        local_cols=["subscription_board_id", "subscription_repo_id"],
        remote_cols=["board_id", "repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="subscribed_lists_list_id_fkey", table_name="subscribed_lists", type_="foreignkey")
    op.drop_constraint(constraint_name="subscribed_lists_subscription_board_id_fkey", table_name="subscribed_lists", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_lists_list_id_fkey",
        source_table="subscribed_lists",
        referent_table="lists",
        local_cols=["list_id"],
        remote_cols=["trello_list_id"]
    )

    op.create_foreign_key(
        constraint_name="subscribed_lists_subscription_board_id_fkey",
        source_table="subscribed_lists",
        referent_table="subscriptions",
        local_cols=["subscription_board_id", "subscription_repo_id"],
        remote_cols=["board_id", "repo_id"]
    )

    pass
