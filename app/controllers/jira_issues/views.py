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

"""jira_issues/views.py

jira_issue-related routes and view-specific logic.
"""

from flask import render_template
from flask_login import login_required
from . import jira_issue
from ...models import JIRAParentIssue, Project, ConfigValue


@jira_issue.route('/<string:key>', methods=['GET'])
@login_required
def index(key):
    """
    Displays JIRA issues pertaining to a particular project.
    """
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    project = Project.query.filter_by(key=key)
    project_id = project[0].id if bool(project) else 0
    project = Project.query.get_or_404(project_id)
    issues = project.parent_issues.order_by(JIRAParentIssue.timestamp.asc())

    return render_template(
        'jira_issues.html',
        project=project,
        issues=issues,
        jira_base_url=ConfigValue.get_or_insert_jira_address()
    )
