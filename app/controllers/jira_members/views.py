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

"""jira_members/views.py

JIRAMember-related routes and view-specific logic.
"""

from os import environ
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import jira_member
from .forms import RefreshForm
from ...models import JIRAMember, ConfigValue
from ...services import JIRAMemberService

jira_member_service = JIRAMemberService()


@jira_member.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the JIRA_members saved on POST request."""
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    form = RefreshForm()
    if form.validate_on_submit():
        jira_member_service.fetch()
        flash('The organization\'s JIRA members have been updated.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = JIRAMember.query
    pagination = query.order_by(JIRAMember.name.asc()).paginate(
        page, per_page=10,
        error_out=False
    )
    jira_members = pagination.items

    return render_template(
        'jira_members.html',
        members=jira_members,
        form=form,
        pagination=pagination,
        organization_name=environ.get('JIRA_SERVER_ADDRESS')
    )
