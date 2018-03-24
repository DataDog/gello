"""Create lists table.

Revision ID: 307445dfeda
Revises: 240c1be6b0d
Create Date: 2018-03-24 17:15:32.564927
"""

from alembic import op
import sqlalchemy as sa

revision = '307445dfeda'
down_revision = '240c1be6b0d'


def upgrade():
    op.create_table(
        'lists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('trello_list_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('board_id', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(['board_id'], ['boards.trello_board_id'], ),
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
