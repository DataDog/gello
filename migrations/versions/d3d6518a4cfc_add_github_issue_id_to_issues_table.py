# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""Add GitHub issue id to issues table.

Revision ID: d3d6518a4cfc
Revises: 6aa929ac04c1
Create Date: 2018-03-27 11:30:15.877206
"""

from alembic import op
import sqlalchemy as sa


revision = 'd3d6518a4cfc'
down_revision = '6aa929ac04c1'


def upgrade():
    op.add_column(
        'issues',
        sa.Column('github_issue_id', sa.Integer(), nullable=False)
    )
    op.create_index(
        'ix_issues_github_issue_id', 'issues', ['github_issue_id'], unique=True
    )


def downgrade():
    op.drop_index('ix_issues_github_issue_id', 'issues')
    op.drop_column('issues', 'github_issue_id')
