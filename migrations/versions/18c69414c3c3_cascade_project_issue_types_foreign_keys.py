
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade project_issue_types foreign keys

Revision ID: 18c69414c3c3
Revises: c02a740fc17d
Create Date: 2022-11-28 20:55:36.892541
"""

from alembic import op
import sqlalchemy as sa


revision = '18c69414c3c3'
down_revision = 'c02a740fc17d'


def upgrade():
    op.drop_constraint(constraint_name="project_issue_types_helper_issue_type_id_fkey", table_name="project_issue_types_helper", type_="foreignkey")
    op.drop_constraint(constraint_name="project_issue_types_helper_project_id_fkey", table_name="project_issue_types_helper", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="project_issue_types_helper_issue_type_id_fkey",
        source_table="project_issue_types_helper",
        referent_table="jira_issue_types",
        local_cols=["issue_type_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="project_issue_types_helper_project_id_fkey",
        source_table="project_issue_types_helper",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="project_issue_types_helper_issue_type_id_fkey", table_name="project_issue_types_helper", type_="foreignkey")
    op.drop_constraint(constraint_name="project_issue_types_helper_project_id_fkey", table_name="project_issue_types_helper", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="project_issue_types_helper_issue_type_id_fkey",
        source_table="project_issue_types_helper",
        referent_table="jira_issue_types",
        local_cols=["issue_type_id"],
        remote_cols=["id"]
    )

    op.create_foreign_key(
        constraint_name="project_issue_types_helper_project_id_fkey",
        source_table="project_issue_types_helper",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"]
    )

    pass
