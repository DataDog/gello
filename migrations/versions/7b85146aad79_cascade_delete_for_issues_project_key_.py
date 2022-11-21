
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade delete for issues project_key foreign key

Revision ID: 7b85146aad79
Revises: 1d125da81dbf
Create Date: 2022-11-21 18:38:32.240352
"""

from alembic import op
import sqlalchemy as sa


revision = '7b85146aad79'
down_revision = '1d125da81dbf'


def upgrade():
    op.drop_constraint(constraint_name="issues_jira_project_key_fkey", table_name="issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="issues_jira_project_key_fkey",
        source_table="issues",
        referent_table="projects",
        local_cols=["jira_project_key"],
        remote_cols=["key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="issues_jira_project_key_fkey", table_name="issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="issues_jira_project_key_fkey",
        source_table="issues",
        referent_table="projects",
        local_cols=["jira_project_key"],
        remote_cols=["key"]
    )

    pass
