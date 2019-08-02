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

import re
import textwrap

from flask import redirect, url_for, flash, request
from flask_login import login_required
from . import subscription
from .forms import NewSubscriptionForm, UpdateForm
from ...services import SubscriptionService
from ...tasks import CreateGitHubWebhook, DeleteGitHubWebhook
from ...models import Repo
from ...models import Subscription

subscription_service = SubscriptionService()


@subscription.route('/create', methods=['POST'])
@login_required
def create():
    create_form = NewSubscriptionForm(request.form)

    if create_form.validate():
        repo_id = create_form.get_repo_id()

        # check if there already exists a webhook with this repository
        repo = Repo.query.filter_by(github_repo_id=repo_id).first()
        if repo.github_webhook_id is None:
            # Enqueue a task to create a webhook for the repo (and persist webhook_id)
            CreateGitHubWebhook.delay(
                url_root=request.url_root,
                repo_id=create_form.get_repo_id()
            )

        subscription_service.create(
            board_id=create_form.get_board_id(),
            repo_id=repo_id,
            issue_autocard=create_form.issue_autocard.data,
            pull_request_autocard=create_form.pull_request_autocard.data
        )
        flash('Created subscription')
        return redirect(url_for('main.index'))
    else:
        flash(
            textwrap.dedent(
                f"""
                Could not create subscription because an error occurred:
                {create_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('main.index'))


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

    # check if no other subscriptions are listening to this repo
    subscriptions = Subscription.query.filter_by(repo_id=repo_id).all()

    if not subscriptions:
        # Enqueue a task to delete the webhook from the repo (and remove webhook_id)
        repo = Repo.query.filter_by(github_repo_id=repo_id).first()
        DeleteGitHubWebhook.delay(
            webhook_id=repo.github_webhook_id,
            repo_id=repo_id
        )

    flash('Deleted subscription')
    return redirect(url_for('main.index'))
