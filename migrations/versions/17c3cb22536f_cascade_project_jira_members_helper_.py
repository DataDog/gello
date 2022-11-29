
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade project_jira_members_helper foreign keys

Revision ID: 17c3cb22536f
Revises: 18c69414c3c3
Create Date: 2022-11-29 21:20:49.176388
"""

from alembic import op
import sqlalchemy as sa


revision = '17c3cb22536f'
down_revision = '18c69414c3c3'


def upgrade():
    op.drop_constraint(constraint_name="project_jira_members_helper_jira_member_id_fkey", table_name="project_jira_members_helper", type_="foreignkey")
    op.drop_constraint(constraint_name="project_jira_members_helper_project_id_fkey", table_name="project_jira_members_helper", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="project_jira_members_helper_jira_member_id_fkey",
        source_table="project_jira_members_helper",
        referent_table="jira_members",
        local_cols=["jira_member_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="project_jira_members_helper_project_id_fkey",
        source_table="project_jira_members_helper",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="project_jira_members_helper_jira_member_id_fkey", table_name="project_jira_members_helper", type_="foreignkey")
    op.drop_constraint(constraint_name="project_jira_members_helper_project_id_fkey", table_name="project_jira_members_helper", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="project_jira_members_helper_jira_member_id_fkey",
        source_table="project_jira_members_helper",
        referent_table="jira_members",
        local_cols=["jira_member_id"],
        remote_cols=["id"]
    )

    op.create_foreign_key(
        constraint_name="project_jira_members_helper_project_id_fkey",
        source_table="project_jira_members_helper",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"]
    )

    pass
