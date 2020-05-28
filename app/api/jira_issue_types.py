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
from ..models import Project
from . import api


@api.route('/jira_issue_types/<string:project_key>')
@login_required
def get_jira_issue_types(project_key):
    jira_issue_type = request.args.get('jira_issue_type', 1, type=int)

    project = Project.query.filter_by(key=project_key).first()

    if not project:
        return jsonify({
            'jira_issue_types': [],
            'prev': None,
            'next': None,
            'count': 0
        })

    pagination = project.issue_types.filter_by(
        subtask=False
    ).paginate(
        jira_issue_type, per_page=100, error_out=False)
    jira_issue_types = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_jira_issue_types',
                       jira_issue_type=jira_issue_type-1,
                       _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_jira_issue_types',
                       jira_issue_type=jira_issue_type+1,
                       _external=True)

    return jsonify(
        {
            'jira_issue_types': [jira_issue_type.to_json()
                          for jira_issue_type in jira_issue_types],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
