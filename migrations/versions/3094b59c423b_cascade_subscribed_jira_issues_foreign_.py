
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade subscribed_jira_issues foreign keys

Revision ID: 3094b59c423b
Revises: fe3134896e13
Create Date: 2022-11-29 21:37:29.796533
"""

from alembic import op
import sqlalchemy as sa


revision = '3094b59c423b'
down_revision = 'fe3134896e13'


def upgrade():
    op.drop_constraint(constraint_name="subscribed_jira_issues_jira_issue_key_fkey", table_name="subscribed_jira_issues", type_="foreignkey")
    # this constraint name might not exist locally because the originally created constraint was not named
    # but this constraint name was taken from the live DB
    op.drop_constraint(constraint_name="subscribed_jira_issues_subscription_project_key_fkey", table_name="subscribed_jira_issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_jira_issues_jira_issue_key_fkey",
        source_table="subscribed_jira_issues",
        referent_table="jira_parent_issues",
        local_cols=["jira_issue_key"],
        remote_cols=["jira_issue_key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="subscribed_jira_issues_subscription_project_key_fkey",
        source_table="subscribed_jira_issues",
        referent_table="subscriptions",
        local_cols=["subscription_project_key", "subscription_repo_id"],
        remote_cols=["project_key", "repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="subscribed_jira_issues_jira_issue_key_fkey", table_name="subscribed_jira_issues", type_="foreignkey")
    op.drop_constraint(constraint_name="subscribed_jira_issues_subscription_project_key_fkey", table_name="subscribed_jira_issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="subscribed_jira_issues_jira_issue_key_fkey",
        source_table="subscribed_jira_issues",
        referent_table="jira_parent_issues",
        local_cols=["jira_issue_key"],
        remote_cols=["jira_issue_key"]
    )

    op.create_foreign_key(
        constraint_name="subscribed_jira_issues_subscription_project_key_fkey",
        source_table="subscribed_jira_issues",
        referent_table="subscriptions",
        local_cols=["subscription_project_key", "subscription_repo_id"],
        remote_cols=["project_key", "repo_id"]
    )

    pass
