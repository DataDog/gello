
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade subscribed_jira_projects foreign keys

Revision ID: 1dfef2c5de0f
Revises: 3094b59c423b
Create Date: 2022-11-29 21:42:09.694628
"""

from alembic import op
import sqlalchemy as sa


revision = '1dfef2c5de0f'
down_revision = '3094b59c423b'


def upgrade():
    op.drop_constraint(constraint_name="subscribed_jira_projects_issue_type_id_fkey", table_name="subscribed_jira_projects", type_="foreignkey")
    op.drop_constraint(constraint_name="subscribed_jira_projects_subscription_project_key_fkey", table_name="subscribed_jira_projects", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_jira_projects_issue_type_id_fkey",
        source_table="subscribed_jira_projects",
        referent_table="jira_issue_types",
        local_cols=["issue_type_id"],
        remote_cols=["issue_type_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="subscribed_jira_projects_subscription_project_key_fkey",
        source_table="subscribed_jira_projects",
        referent_table="subscriptions",
        local_cols=["subscription_project_key", "subscription_repo_id"],
        remote_cols=["project_key", "repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="subscribed_jira_projects_issue_type_id_fkey", table_name="subscribed_jira_projects", type_="foreignkey")
    op.drop_constraint(constraint_name="subscribed_jira_projects_subscription_project_key_fkey", table_name="subscribed_jira_projects", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_jira_projects_issue_type_id_fkey",
        source_table="subscribed_jira_projects",
        referent_table="jira_issue_types",
        local_cols=["issue_type_id"],
        remote_cols=["issue_type_id"]
    )

    op.create_foreign_key(
        constraint_name="subscribed_jira_projects_subscription_project_key_fkey",
        source_table="subscribed_jira_projects",
        referent_table="subscriptions",
        local_cols=["subscription_project_key", "subscription_repo_id"],
        remote_cols=["project_key", "repo_id"]
    )

    pass
