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

"""api/projects.py

Exposed projects for autocomplete.
"""

from flask import jsonify, request, url_for
from flask_login import login_required
from ..models import Project
from . import api


@api.route('/projects/')
@login_required
def get_projects():
    project = request.args.get('project', 1, type=int)

    pagination = Project.query.paginate(project, per_page=100, error_out=False)
    projects = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_projects', project=project-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_projects', project=project+1, _external=True)

    return jsonify(
        {
            'projects': [project.to_json() for project in projects],
            'prev': prev,
            'next': next,
            'count': pagination.total
        }
    )
