"""Create repos table

Revision ID: 51c2b3a12ae
Revises: 3b9f644c80e
Create Date: 2018-03-22 12:58:49.301489
"""

from alembic import op
import sqlalchemy as sa


revision = '51c2b3a12ae'
down_revision = '3b9f644c80e'


def upgrade():
    op.create_table(
        'repos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('url', sa.String(length=64), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_repos_timestamp', 'repos', ['timestamp'], unique=False)


def downgrade():
    op.drop_index('ix_repos_timestamp', 'repos')
    op.drop_table('repos')
