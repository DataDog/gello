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

"""jira_issue_types/views.py

jira_issue_type-related routes and view-specific logic.
"""

from flask import render_template
from flask_login import login_required
from . import jira_issue_type
from ...models import JIRAIssueType, Project, ConfigValue


@jira_issue_type.route('/<string:key>', methods=['GET'])
@login_required
def index(key):
    """
    Displays JIRA issue types pertaining to a particular project.
    """
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    project = Project.query.filter_by(key=key)
    project_id = project[0].id if bool(project) else 0
    project = Project.query.get_or_404(project_id)
    issue_types = project.issue_types.order_by(JIRAIssueType.timestamp.asc())

    return render_template(
        'jira_issue_types.html',
        project=project,
        issue_types=issue_types,
        jira_base_url=ConfigValue.get_or_insert_jira_address()
    )
