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

"""github_members/views.py

GitHubMembers-related routes and view-specific logic.
"""

from os import environ
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import github_member
from .forms import RefreshForm
from ...models import GitHubMember
from ...services import GitHubMemberService

github_member_service = GitHubMemberService()


@github_member.route('/<string:base>', methods=['GET', 'POST'])
@login_required
def index(base):
    """Updates the github_members saved on POST request."""
    form = RefreshForm()
    if form.validate_on_submit():
        github_member_service.fetch()
        flash('The organization\'s GitHub members have been updated.')
        return redirect(url_for('.index', base=base))

    page = request.args.get('page', 1, type=int)
    query = GitHubMember.query
    pagination = query.order_by(GitHubMember.login.asc()).paginate(
        page,
        per_page=10,
        error_out=False
    )
    github_members = pagination.items

    return render_template(
        'github_members.html',
        members=github_members,
        form=form,
        pagination=pagination,
        organization_name=environ.get('GITHUB_ORG_LOGIN'),
        base=base
    )
