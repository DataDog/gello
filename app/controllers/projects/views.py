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

"""boards/views.py

Boards-related routes and view-specific logic.
"""

from os import environ
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import project
from .forms import RefreshForm
from ...models import Project, ConfigValue
from ...tasks.fetch_jira_projects import FetchJIRAProjects


@project.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the projects and corresponding issues saved on POST request."""
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    form = RefreshForm()
    if form.validate_on_submit():
        FetchJIRAProjects.delay()
        flash('The projects are being updated. Please do not click the Refresh projects button again. This may take a several minutes...')

        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Project.query
    pagination = query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=10,
        error_out=False
    )
    projects = pagination.items

    return render_template(
        'projects.html',
        projects=projects,
        form=form,
        pagination=pagination,
        organization_name=environ.get('GITHUB_ORG_LOGIN'),
        jira_base_url=ConfigValue.get_or_insert_jira_address()
    )
