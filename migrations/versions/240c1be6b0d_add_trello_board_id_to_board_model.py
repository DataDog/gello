"""Add trello_board_id to Board model.

Revision ID: 240c1be6b0d
Revises: 391a5fb9ba3
Create Date: 2018-03-24 13:26:48.326446
"""

from alembic import op
import sqlalchemy as sa


revision = '240c1be6b0d'
down_revision = '391a5fb9ba3'


def upgrade():
    op.add_column(
        'boards',
        sa.Column('trello_board_id', sa.String(length=64), nullable=False)
    )
    op.create_index(
        'ix_boards_trello_board_id', 'boards', ['trello_board_id'], unique=True
    )


def downgrade():
    op.drop_index('ix_boards_trello_board_id', 'boards')
    op.drop_column('boards', 'trello_board_id')
