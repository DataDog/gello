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

from flask import render_template, request, redirect, url_for
from . import main
from ...tasks import GitHubReceiver
from ...models import Subscription, ConfigValue
from app.controllers.subscriptions.forms import NewSubscriptionForm, \
    UpdateForm, DeleteForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """Updates the repositories saved on POST request."""
    # Creation form logic
    if request.method == 'POST':
        GitHubReceiver.delay(payload=json.loads(request.get_data()))
        return "GitHub event received."

    if ConfigValue.query.get('TRELLO_ORG_NAME'):
        create_form = NewSubscriptionForm()
        page = request.args.get('page', 1, type=int)
        query = Subscription.query.filter(Subscription.board_id.isnot(None))
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
    else:
        return redirect(url_for('onboarding.index'))
