"""Add github_repo_id to Repo model.

Revision ID: 56d8a1d3682
Revises: 307445dfeda
Create Date: 2018-03-25 12:14:12.203175
"""

from alembic import op
import sqlalchemy as sa


revision = '56d8a1d3682'
down_revision = '307445dfeda'


def upgrade():
    op.add_column(
        'repos',
        sa.Column('github_repo_id', sa.Integer(), nullable=False)
    )
    op.create_index(
        'ix_repos_github_repo_id', 'repos', ['github_repo_id'], unique=True
    )


def downgrade():
    op.drop_index('ix_repos_github_repo_id', 'repos')
    op.drop_column('repos', 'github_repo_id')
