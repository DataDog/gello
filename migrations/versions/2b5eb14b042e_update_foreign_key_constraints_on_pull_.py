"""Update foreign key constraints on pull_requests and issues.

Revision ID: 2b5eb14b042e
Revises: 23f172a581d1
Create Date: 2018-03-27 12:13:56.248038
"""

from alembic import op


revision = '2b5eb14b042e'
down_revision = '23f172a581d1'


def upgrade():
    op.create_foreign_key(
        'fk_issues_repo_id_repos',
        'issues', 'repos',
        ['repo_id'], ['github_repo_id'],
    )
    op.create_foreign_key(
        'fk_pull_requests_repo_id_repos',
        'pull_requests', 'repos',
        ['repo_id'], ['github_repo_id'],
    )


def downgrade():
    op.drop_constraint('fk_issues_repo_id_repos', 'issues', type_='foreignkey')
    op.drop_constraint(
        'fk_pull_requests_repo_id_repos', 'issues', type_='foreignkey'
    )
