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

"""repos/views.py

repos-related routes and view-specific logic.
"""

from os import environ
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import repo
from .forms import RefreshForm
from ...models import Repo
from ...services import RepoService

repo_service = RepoService()


@repo.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the repositories saved on POST request."""
    form = RefreshForm()
    if form.validate_on_submit():
        repo_service.fetch()
        flash('The repos have been updated.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Repo.query
    pagination = query.order_by(Repo.timestamp.desc()).paginate(
        page, per_page=10, error_out=False
    )
    repos = pagination.items

    return render_template(
        'repos.html',
        repos=repos,
        form=form,
        pagination=pagination,
        organization_name=environ.get('GITHUB_ORG_LOGIN')
    )
