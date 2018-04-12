#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""Add 'webhooks_active' boolean column for the 'boards' table.

Revision ID: b29020d2c4f2
Revises: bde502a0cc6f
Create Date: 2018-04-12 14:31:16.095813
"""

from alembic import op
import sqlalchemy as sa


revision = 'b29020d2c4f2'
down_revision = 'bde502a0cc6f'


def upgrade():
    op.add_column(
        'boards',
        sa.Column(
            'webhooks_active', sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )


def downgrade():
    op.drop_column('boards', 'webhooks_active')
