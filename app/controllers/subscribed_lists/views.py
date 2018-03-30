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

from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from . import subscribed_list
from .forms import NewForm, DeleteForm
from ...services import SubscribedListService
from ...models import Subscription, SubscribedList

subscribed_list_service = SubscribedListService()


@subscribed_list.route('/<string:board_id>/<int:repo_id>', methods=['GET', 'POST'])
@login_required
def index(board_id, repo_id):
    """
    Displays trello lists pertaining to a particular subscription.
    """
    # Creation form logic
    create_form = NewForm(board_id)
    if create_form.validate_on_submit():
        subscribed_list_service.create(
            board_id=board_id,
            repo_id=repo_id,
            list_id=create_form.list_id.data
        )

        flash('Created subscription')
        return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))

    subscription = Subscription.query.get_or_404([board_id, repo_id])
    lists = subscription.subscribed_lists.order_by(SubscribedList.timestamp.asc())
    list_form_pairs = [(l, DeleteForm()) for l in lists]

    return render_template(
        'subscribed_lists.html',
        create_form=create_form,
        subscription=subscription,
        list_form_pairs=list_form_pairs
    )


@subscribed_list.route('/<string:board_id>/<int:repo_id>/<string:list_id>/delete',
                       methods=['POST'])
@login_required
def delete(board_id, repo_id, list_id):
    subscribed_list_service.delete(board_id, repo_id, list_id)
    flash('Deleted subscription')
    return redirect(url_for('.index', board_id=board_id, repo_id=repo_id))
