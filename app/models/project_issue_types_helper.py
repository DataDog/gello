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

"""models/project_issues_table.py

Helper table for projects->issue_types many-to-many relationship
"""

from .. import db


# Helper table for projects -> issue_types many-to-many relationship
project_issue_types_helper = db.Table(
    'project_issue_types_helper',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'),
              primary_key=True),
    db.Column('issue_type_id', db.Integer,
              db.ForeignKey('jira_issue_types.id'), primary_key=True)
)
