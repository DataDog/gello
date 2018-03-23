"""Create pull requests table

Revision ID: 52460a6cc39
Revises: 440cec339d0
Create Date: 2018-03-22 17:14:39.280751
"""

from alembic import op
import sqlalchemy as sa


revision = '52460a6cc39'
down_revision = '440cec339d0'


def upgrade():
    op.create_table(
        'pull_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('url', sa.String(length=64), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('repo_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['repo_id'], ['repos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_pull_request_timestamp', 'pull_requests', ['timestamp'], unique=False
    )


def downgrade():
    op.drop_index('ix_pull_request_timestamp', 'pull_requests')
    op.drop_table('pull_requests')
