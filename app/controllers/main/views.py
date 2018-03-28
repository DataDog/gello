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
from flask import render_template, request, current_app
from . import main
from ...tasks import GitHubReceiver
from ...models import Repo, Subscription


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        GitHubReceiver.delay(payload=json.loads(request.get_data()))
        return "GitHub event received."

    page = request.args.get('page', 1, type=int)

    # Display the subscribed repositories in the home view
    subscription_ids = [r.repo_id for r in Subscription.query]
    query = Repo.query.filter(Repo.github_repo_id.in_(subscription_ids))
    pagination = query.order_by(Repo.timestamp.desc()).paginate(
        page, per_page=10, error_out=False
    )
    subscribed_repos = pagination.items

    return render_template(
        'index.html',
        subscribed_repos=subscribed_repos,
        pagination=pagination,
        organization_name=current_app.config.get('GITHUB_ORG_LOGIN')
    )
