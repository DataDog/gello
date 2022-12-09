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

def swap_value_and_label(project):
    value = project.value

    return {
        label: value,
        value: value,
    }


@api.route('/projects/')
@login_required
def get_projects():
    project_string = request.args.get('project')

    projects_by_key = Project.query.filter(Project.key.like('%%{0}%%'.format(project_string))).all()

    projects_by_name = Project.query.filter(Project.name.ilike('%%{0}%%'.format(project_string))).all()

    projects_by_key_formatted = [project.to_autocomplete() for project in projects_by_key]

    projects_by_name_formatted = [project.to_json() for project in projects_by_name]

    projects = projects_by_key_formatted + projects_by_name_formatted

    return jsonify(
        {
            'projects': projects
        }
    )
