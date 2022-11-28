
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade more foreign keys

Revision ID: f830b2fcf2bf
Revises: 7b85146aad79
Create Date: 2022-11-28 18:58:13.772999
"""

from alembic import op
import sqlalchemy as sa


revision = 'f830b2fcf2bf'
down_revision = '7b85146aad79'


# TODO: Edit this to use the proper foreign key constraints

def upgrade():
    op.drop_constraint(constraint_name="issues_jira_parent_issue_key_fkey", table_name="issues", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_issues_repo_id_repos", table_name="issues", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_issues_trello_list_id_lists", table_name="issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="issues_jira_parent_issue_key_fkey",
        source_table="issues",
        referent_table="jira_parent_issues",
        local_cols=["jira_parent_issue_key"],
        remote_cols=["jira_issue_key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="fk_issues_repo_id_repos",
        source_table="issues",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="fk_issues_trello_list_id_lists",
        source_table="issues",
        referent_table="lists",
        local_cols=["trello_list_id"],
        remote_cols=["trello_list_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="issues_jira_parent_issue_key_fkey", table_name="issues", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_issues_repo_id_repos", table_name="issues", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_issues_trello_list_id_lists", table_name="issues", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="issues_jira_parent_issue_key_fkey",
        source_table="issues",
        referent_table="jira_parent_issues",
        local_cols=["jira_parent_issue_key"],
        remote_cols=["jira_issue_key"]
    )

    op.create_foreign_key(
        constraint_name="fk_issues_repo_id_repos",
        source_table="issues",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"]
    )

    op.create_foreign_key(
        constraint_name="fk_issues_trello_list_id_lists",
        source_table="issues",
        referent_table="lists",
        local_cols=["trello_list_id"],
        remote_cols=["trello_list_id"]
    )

    pass
