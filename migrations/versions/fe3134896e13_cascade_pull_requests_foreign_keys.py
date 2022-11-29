
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""cascade pull_requests foreign keys

Revision ID: fe3134896e13
Revises: 17c3cb22536f
Create Date: 2022-11-29 21:25:55.211880
"""

from alembic import op
import sqlalchemy as sa


revision = 'fe3134896e13'
down_revision = '17c3cb22536f'


def upgrade():
    op.drop_constraint(constraint_name="fk_pull_requests_repo_id_repos", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_pull_requests_trello_list_id_lists", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="pull_requests_jira_parent_issue_key_fkey", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="pull_requests_jira_project_key_fkey", table_name="pull_requests", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="fk_pull_requests_repo_id_repos",
        source_table="pull_requests",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="fk_pull_requests_trello_list_id_lists",
        source_table="pull_requests",
        referent_table="lists",
        local_cols=["trello_list_id"],
        remote_cols=["trello_list_id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="pull_requests_jira_parent_issue_key_fkey",
        source_table="pull_requests",
        referent_table="projects",
        local_cols=["jira_parent_issue_key"],
        remote_cols=["jira_issue_key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    op.create_foreign_key(
        constraint_name="pull_requests_jira_project_key_fkey",
        source_table="pull_requests",
        referent_table="projects",
        local_cols=["jira_project_key"],
        remote_cols=["key"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(constraint_name="fk_pull_requests_repo_id_repos", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="fk_pull_requests_trello_list_id_lists", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="pull_requests_jira_parent_issue_key_fkey", table_name="pull_requests", type_="foreignkey")
    op.drop_constraint(constraint_name="pull_requests_jira_project_key_fkey", table_name="pull_requests", type_="foreignkey")

    op.create_foreign_key(
        constraint_name="fk_pull_requests_repo_id_repos",
        source_table="pull_requests",
        referent_table="repos",
        local_cols=["repo_id"],
        remote_cols=["github_repo_id"]
    )

    op.create_foreign_key(
        constraint_name="fk_pull_requests_trello_list_id_lists",
        source_table="pull_requests",
        referent_table="lists",
        local_cols=["trello_list_id"],
        remote_cols=["trello_list_id"]
    )

    op.create_foreign_key(
        constraint_name="pull_requests_jira_parent_issue_key_fkey",
        source_table="pull_requests",
        referent_table="projects",
        local_cols=["jira_parent_issue_key"],
        remote_cols=["jira_issue_key"]
    )

    op.create_foreign_key(
        constraint_name="pull_requests_jira_project_key_fkey",
        source_table="pull_requests",
        referent_table="projects",
        local_cols=["jira_project_key"],
        remote_cols=["key"]
    )

    pass
