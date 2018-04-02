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

"""trello_members/views.py

Trello_Members-related routes and view-specific logic.
"""

from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required
from . import trello_member
from .forms import RefreshForm
from ...models import TrelloMember
from ...services import TrelloMemberService

trello_member_service = TrelloMemberService()


@trello_member.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Updates the trello_members saved on POST request."""
    form = RefreshForm()
    if form.validate_on_submit():
        trello_member_service.fetch()
        flash('The organization\'s Trello members have been updated.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = TrelloMember.query
    pagination = query.order_by(TrelloMember.name.asc()).paginate(
        page, per_page=10,
        error_out=False
    )
    trello_members = pagination.items

    return render_template(
        'trello_members.html',
        members=trello_members,
        form=form,
        pagination=pagination,
        organization_name=current_app.config.get('TRELLO_ORG_NAME')
    )
