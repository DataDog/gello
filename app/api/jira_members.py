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

"""api/jira_members.py

Exposed jira_members for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import Project
from . import api


@api.route('/jira_members/<string:project_key>')
@login_required
def get_jira_members(project_key):
    jira_member = request.args.get('jira_member', 1, type=int)

    pagination = Project.query.filter_by(
                    key=project_key
                 ).first().allowed_members.paginate(
        jira_member, per_page=1000, error_out=False
    )
    jira_members = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for(
            'api.get_jira_members',
            jira_member=jira_member-1,
            _external=True
        )

    next = None
    if pagination.has_next:
        next = url_for(
            'api.get_jira_members',
            jira_member=jira_member+1,
            _external=True
        )

    return jsonify(
        {
            'jira_members': [jm.to_json() for jm in jira_members],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
