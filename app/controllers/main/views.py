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

"""main/views.py

repos-related routes and view-specific logic.
"""

import json
import re
import textwrap

from flask import render_template, request, url_for, flash, redirect
from . import main
from ...tasks import GitHubReceiver, CreateGitHubWebhook
from ...models import Subscription
from ...services import SubscriptionService
from app.controllers.subscriptions.forms import NewSubscriptionForm, \
    UpdateForm, DeleteForm

subscription_service = SubscriptionService()


@main.route('/', methods=['GET', 'POST'])
def index():
    """Updates the repositories saved on POST request."""
    # Creation form logic
    create_form = NewSubscriptionForm()
    if create_form.validate_on_submit():
        ids = create_form.list_ids.data
        list_ids = re.split("\s*,\s*", ids.strip()) if ids else []

        subscription_service.create(
            board_id=create_form.get_board_id(),
            repo_id=create_form.get_repo_id(),
            issue_autocard=create_form.issue_autocard.data,
            pull_request_autocard=create_form.pull_request_autocard.data,
            list_ids=list_ids
        )

        # Enqueue a task to create a repository webhook for the repo
        CreateGitHubWebhook.delay(
            url_root=request.url_root,
            repo_id=create_form.get_repo_id()
        )

        flash('Created subscription')
        return redirect(url_for('.index'))
    elif request.method == 'POST':
        flash(
            textwrap.dedent(
                f"""
                Could not create subscription because an error occurred:
                {create_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Subscription.query
    pagination = query.order_by(Subscription.timestamp.desc()).paginate(
        page, per_page=10,
        error_out=False
    )
    subscriptions = pagination.items
    subscription_forms_tuples = [
        (
            s,
            UpdateForm(
                issue_autocard=s.issue_autocard,
                pull_request_autocard=s.pull_request_autocard
            ),
            DeleteForm()
        ) for s in subscriptions
    ]

    return render_template(
        'index.html',
        create_form=create_form,
        subscription_forms_tuples=subscription_forms_tuples,
        pagination=pagination
    )


@main.route('/webhooks', methods=['POST'])
def webhooks():
    """Handle GitHub webhooks."""
    GitHubReceiver.delay(payload=json.loads(request.get_data()))
    return "GitHub event received."
