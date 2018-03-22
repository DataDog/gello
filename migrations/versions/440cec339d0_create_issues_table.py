"""Create issues table

Revision ID: 440cec339d0
Revises: 51c2b3a12ae
Create Date: 2018-03-22 16:48:39.388977
"""

from alembic import op
import sqlalchemy as sa


revision = '440cec339d0'
down_revision = '51c2b3a12ae'


def upgrade():
    op.create_table(
        'issues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('url', sa.String(length=64), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('repo_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['repo_id'], ['repos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_issues_timestamp', 'issues', ['timestamp'], unique=False
    )


def downgrade():
    op.drop_index('ix_issues_timestamp', 'issues')
    op.drop_table('issues')
