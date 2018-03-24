"""Create lists table

Revision ID: 391a5fb9ba3
Revises: 57bc1ebd1cc
Create Date: 2018-03-24 13:02:21.181080
"""

from alembic import op
import sqlalchemy as sa


revision = '391a5fb9ba3'
down_revision = '57bc1ebd1cc'


def upgrade():
    op.create_table(
        'lists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('trello_list_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('board_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_lists_trello_list_id', 'lists', ['trello_list_id'], unique=True
    )
    op.create_index(
        'ix_lists_timestamp', 'lists', ['timestamp'], unique=False
    )


def downgrade():
    op.drop_index('ix_lists_timestamp', 'lists')
    op.drop_index('ix_lists_trello_list_id', 'lists')
    op.drop_table('lists')
