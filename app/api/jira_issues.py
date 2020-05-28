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

"""api/jira_issues.py

Exposed jira_issues for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import JIRAParentIssue
from . import api


@api.route('/jira_issues/<string:project_key>')
@login_required
def get_jira_issues(project_key):
    jira_issue = request.args.get('jira_issue', 1, type=int)

    pagination = JIRAParentIssue.query.filter_by(project_key=project_key).paginate(
        jira_issue, per_page=100, error_out=False)
    jira_issues = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_jira_issues', jira_issue=jira_issue-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_jira_issues', jira_issue=jira_issue+1, _external=True)

    return jsonify(
        {
            'jira_issues': [jira_issue.to_json() for jira_issue in jira_issues],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
