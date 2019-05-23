
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""add webhooks in repos and subscriptions

Revision ID: ab02ccdd853d
Revises: bde502a0cc6f
Create Date: 2019-05-22 17:36:04.673041
"""

from alembic import op
import sqlalchemy as sa


revision = 'ab02ccdd853d'
down_revision = 'bde502a0cc6f'


def upgrade():
    op.add_column(
        'repos',
        sa.Column('github_webhook_id', sa.Integer, nullable=True)
    )

def downgrade():
    op.drop_column('repos', 'github_repo_id')

