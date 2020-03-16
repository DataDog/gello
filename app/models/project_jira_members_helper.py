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

"""models/project_jira_members_helper.py

Helper table for projects->jira_members many-to-many relationship
"""

from .. import db


# Helper table for projects -> jira_members many-to-many relationship
project_jira_members_helper = db.Table(
    'project_jira_members_helper',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'),
              primary_key=True),
    db.Column('jira_member_id', db.Integer,
              db.ForeignKey('jira_members.id'), primary_key=True)
)
