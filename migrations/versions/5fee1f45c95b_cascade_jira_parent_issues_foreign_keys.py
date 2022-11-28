
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade jira_parent_issues foreign keys

Revision ID: 5fee1f45c95b
Revises: f830b2fcf2bf
Create Date: 2022-11-28 20:30:26.059558
"""

from alembic import op
import sqlalchemy as sa


revision = '5fee1f45c95b'
down_revision = 'f830b2fcf2bf'


def upgrade():
    op.drop_constraint(constraint_name="jira_parent_issues_project_key_fkey", table_name="jira_parent_issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="jira_parent_issues_project_key_fkey",
        source_table="jira_parent_issues",
        referent_table="projects",
        local_cols=["project_key"],
        remote_cols=["key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="jira_parent_issues_project_key_fkey", table_name="jira_parent_issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="jira_parent_issues_project_key_fkey",
        source_table="jira_parent_issues",
        referent_table="projects",
        local_cols=["project_key"],
        remote_cols=["key"]
    )

    pass
