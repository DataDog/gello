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

"""subscriptions/views.py

subscriptions-related routes and view-specific logic.
"""


from flask import redirect, url_for, flash, request
from flask_login import login_required
from . import subscription
from .forms import UpdateForm
from ...services import SubscriptionService

subscription_service = SubscriptionService()


@subscription.route('/<string:board_id>/<int:repo_id>/update', methods=['POST'])
@login_required
def update(board_id, repo_id):
    form = UpdateForm(request.form)

    subscription_service.update(
        board_id=board_id,
        repo_id=repo_id,
        issue_autocard=form.issue_autocard.data,
        pull_request_autocard=form.pull_request_autocard.data
    )
    flash('Updated subscription')

    return redirect(url_for('main.index'))


@subscription.route('/<string:board_id>/<int:repo_id>/delete', methods=['POST'])
@login_required
def delete(board_id, repo_id):
    subscription_service.delete(board_id, repo_id)
    flash('Deleted subscription')
    return redirect(url_for('main.index'))
