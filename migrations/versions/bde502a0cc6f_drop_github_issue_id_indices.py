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

"""Drop github_issue_id indices.

Revision ID: bde502a0cc6f
Revises: 97c9100c8b46
Create Date: 2018-04-04 13:21:24.500871
"""

from alembic import op


revision = 'bde502a0cc6f'
down_revision = '97c9100c8b46'


def upgrade():
    op.drop_index('ix_pull_requests_github_pull_request_id', 'pull_requests')
    op.drop_index('ix_issues_github_issue_id', 'issues')


def downgrade():
    op.create_index(
        'ix_issues_github_issue_id', 'issues', ['github_issue_id'], unique=True
    )
    op.create_index(
        'ix_pull_requests_github_pull_request_id',
        'pull_requests',
        ['github_pull_request_id'],
        unique=True
    )
