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

"""subscribed_lists/views.py

subscribed_lists-related routes and view-specific logic.
"""

import textwrap

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from . import subscribed_list
from .forms import NewForm, UpdateForm, DeleteForm
from ...services import SubscribedListService
from ...models import Subscription, SubscribedList, TrelloMember, ConfigValue

subscribed_list_service = SubscribedListService()


@subscribed_list.route(
    '/<string:board_id>/<int:repo_id>',
    methods=['GET', 'POST']
)
@login_required
def index(board_id, repo_id):
    """
    Displays trello lists pertaining to a particular subscription.
    """
    # Creation form logic
    create_form = NewForm(board_id, repo_id)
    if create_form.validate_on_submit():
        username = create_form.trello_username.data.strip()
        member_id = create_form.get_trello_member_id() if username else None

        subscribed_list_service.create(
            board_id=board_id,
            repo_id=repo_id,
            list_id=create_form.get_list_id(),
            trello_member_id=member_id
        )

        flash('Created subscription')
        return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))
    elif request.method == 'POST':
        flash(
            textwrap.dedent(
                f"""
                Could not create subscribed list because an error occurred:
                {create_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))

    if not ConfigValue.query.get('TRELLO_ORG_NAME'):
        return redirect(url_for('onboarding.index'))

    sub_id = Subscription.query.filter_by(
        board_id=board_id, repo_id=repo_id
    ).first()
    sub_id = 0 if not bool(sub_id) else sub_id.id

    subscription = Subscription.query.get_or_404([sub_id, repo_id])
    lists = subscription.subscribed_lists.order_by(
        SubscribedList.timestamp.asc()
    )

    list_form_pairs = []
    for l in lists:
        member = TrelloMember.query.filter_by(
            trello_member_id=l.trello_member_id).first()

        if member:
            update_form = UpdateForm(trello_update_username=member.username)
        else:
            update_form = UpdateForm()

        list_form_pairs.append((l, update_form, DeleteForm()))

    return render_template(
        'subscribed_lists.html',
        create_form=create_form,
        subscription=subscription,
        list_form_pairs=list_form_pairs
    )


@subscribed_list.route(
    '/<string:board_id>/<int:repo_id>/<string:list_id>/update',
    methods=['POST']
)
@login_required
def update(board_id, repo_id, list_id):
    update_form = UpdateForm(request.form)

    if update_form.validate():
        username = update_form.trello_update_username.data.strip()
        member_id = update_form.get_trello_member_id() if username else None

        subscribed_list_service.update(
            board_id=board_id,
            repo_id=repo_id,
            list_id=list_id,
            trello_member_id=member_id
        )

        flash('Updated subscription')
        return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))
    else:
        flash(
            textwrap.dedent(
                f"""
                Could not update subscribed list because an error occurred:
                {update_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))


@subscribed_list.route(
    '/<string:board_id>/<int:repo_id>/<string:list_id>/delete',
    methods=['POST']
)
@login_required
def delete(board_id, repo_id, list_id):
    subscribed_list_service.delete(board_id, repo_id, list_id)
    flash('Deleted subscription')
    return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))
