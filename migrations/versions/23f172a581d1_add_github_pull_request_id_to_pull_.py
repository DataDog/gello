"""Add GitHub pull_request id to pull_requests table.

Revision ID: 23f172a581d1
Revises: d3d6518a4cfc
Create Date: 2018-03-27 11:32:49.581106
"""

from alembic import op
import sqlalchemy as sa


revision = '23f172a581d1'
down_revision = 'd3d6518a4cfc'


def upgrade():
    op.add_column(
        'pull_requests',
        sa.Column('github_pull_request_id', sa.Integer(), nullable=False)
    )
    op.create_index(
        'ix_pull_requests_github_pull_request_id',
        'pull_requests',
        ['github_pull_request_id'],
        unique=True
    )


def downgrade():
    op.drop_index('ix_pull_requests_github_pull_request_id', 'pull_requests')
    op.drop_column('pull_requests', 'github_pull_request_id')
