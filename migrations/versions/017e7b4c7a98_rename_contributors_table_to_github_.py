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

"""Rename contributors table to github_members.

Revision ID: 017e7b4c7a98
Revises: 3b6e7f250153
Create Date: 2018-04-02 10:38:55.061234
"""

from alembic import op


revision = '017e7b4c7a98'
down_revision = '3b6e7f250153'


def upgrade():
    op.rename_table('contributors', 'github_members')


def downgrade():
    op.rename_table('github_members', 'contributors')
