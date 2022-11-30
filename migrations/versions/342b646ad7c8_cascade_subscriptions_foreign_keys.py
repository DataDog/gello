
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade subscriptions foreign keys

Revision ID: 342b646ad7c8
Revises: 8ef81fc51dc0
Create Date: 2022-11-29 21:50:10.199802
"""

from alembic import op
import sqlalchemy as sa


revision = '342b646ad7c8'
down_revision = '8ef81fc51dc0'


def upgrade():
    op.drop_constraint(constraint_name="subscriptions_board_id_fkey", table_name="subscriptions", type_="foreignkey")
    op.drop_constraint(constraint_name="subscriptions_project_key_fkey", table_name="subscriptions", type_="foreignkey")
    op.drop_constraint(constraint_name="subscriptions_repo_id_fkey", table_name="subscriptions", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscriptions_board_id_fkey",
        source_table="subscriptions",
        referent_table="boards",
        local_cols=["board_id"],
        remote_cols=["trello_board_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="subscriptions_project_key_fkey",
        source_table="subscriptions",
        referent_table="projects",
        local_cols=["project_key"],
        remote_cols=["key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="subscriptions_repo_id_fkey",
        source_table="subscriptions",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="subscriptions_board_id_fkey", table_name="subscriptions", type_="foreignkey")
    op.drop_constraint(constraint_name="subscriptions_project_key_fkey", table_name="subscriptions", type_="foreignkey")
    op.drop_constraint(constraint_name="subscriptions_repo_id_fkey", table_name="subscriptions", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscriptions_board_id_fkey",
        source_table="subscriptions",
        referent_table="boards",
        local_cols=["board_id"],
        remote_cols=["trello_board_id"]
    )

    op.create_foreign_key(
        constraint_name="subscriptions_project_key_fkey",
        source_table="subscriptions",
        referent_table="projects",
        local_cols=["project_key"],
        remote_cols=["key"]
    )

    op.create_foreign_key(
        constraint_name="subscriptions_repo_id_fkey",
        source_table="subscriptions",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"]
    )

    pass
