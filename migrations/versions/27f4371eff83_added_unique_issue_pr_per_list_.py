
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""added unique issue/pr-per-list constraint in issues and PRs

Revision ID: 27f4371eff83
Revises: ab02ccdd853d
Create Date: 2019-05-28 16:35:04.307851
"""

from alembic import op
import sqlalchemy as sa


revision = '27f4371eff83'
down_revision = 'ab02ccdd853d'


def upgrade():
    op.add_column(
        'issues',
        sa.Column('trello_list_id', sa.String(length=64), nullable=True)
    )
    op.create_foreign_key(
        'fk_issues_trello_list_id_lists',
        'issues', 'lists',
        ['trello_list_id'], ['trello_list_id']
    )
    op.create_unique_constraint(
        'uq_issues_list', 'issues',
        ['trello_list_id', 'github_issue_id']
    )

    op.add_column(
        'pull_requests',
        sa.Column('trello_list_id', sa.String(length=64), nullable=True)
    )
    op.create_foreign_key(
        'fk_pull_requests_trello_list_id_lists',
        'pull_requests', 'lists',
        ['trello_list_id'], ['trello_list_id']
    )
    op.create_unique_constraint(
        'uq_pull_requests_list', 'pull_requests',
        ['trello_list_id', 'github_pull_request_id']
    )


def downgrade():
    op.drop_constraint(
        'uq_pull_requests_list', 'pull_requests', type_='unique'
    )
    op.drop_constraint(
        'fk_pull_requests_trello_list_id_lists', 'pull_requests', type_='foreignkey'
    )
    op.drop_column('pull_requests', 'trello_list_id')

    op.drop_constraint(
        'uq_issues_list', 'issues', type_='unique'
    )
    op.drop_constraint(
        'fk_issues_trello_list_id_lists', 'issues', type_='foreignkey'
    )
    op.drop_column('issues', 'trello_list_id')


