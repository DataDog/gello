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

"""jira_subscriptions/views.py

JIRA subscriptions-related routes and view-specific logic.
"""

import textwrap

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import jira_subscription
from .forms import NewSubscriptionForm, UpdateForm, DeleteForm
from ...services import JIRASubscriptionService
from ...tasks import CreateGitHubWebhook, DeleteGitHubWebhook
from ...models import Repo
from ...models import Subscription, ConfigValue

subscription_service = JIRASubscriptionService()


@jira_subscription.route('/', methods=['GET'])
def index():
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    create_form = NewSubscriptionForm()
    page = request.args.get('page', 1, type=int)
    query = Subscription.query.filter(Subscription.project_key.isnot(None))
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
        'jira_subscriptions.html',
        create_form=create_form,
        subscription_forms_tuples=subscription_forms_tuples,
        pagination=pagination,
        jira_base_url=ConfigValue.get_or_insert_jira_address()
    )


@jira_subscription.route('/create', methods=['POST'])
@login_required
def create():
    create_form = NewSubscriptionForm(request.form)

    if create_form.validate():
        issue_keys = create_form.get_issue_keys()
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
            project_key=create_form.get_project_key(),
            repo_id=repo_id,
            issue_autocard=create_form.issue_autocard.data,
            pull_request_autocard=create_form.pull_request_autocard.data,
            issue_type=create_form.get_issue_type().issue_type_id,
            issue_keys=issue_keys
        )
        flash('Created subscription')
        return redirect(url_for('jira_subscription.index'))
    else:
        flash(
            textwrap.dedent(
                f"""
                Could not create subscription because an error occurred:
                {create_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('jira_subscription.index'))


@jira_subscription.route('/<string:project_key>/<int:repo_id>/update', methods=['POST'])
@login_required
def update(project_key, repo_id):
    form = UpdateForm(request.form)

    subscription_service.update(
        project_key=project_key,
        repo_id=repo_id,
        issue_autocard=form.issue_autocard.data,
        pull_request_autocard=form.pull_request_autocard.data
    )
    flash('Updated subscription')

    return redirect(url_for('jira_subscription.index'))


@jira_subscription.route('/<string:project_key>/<int:repo_id>/delete', methods=['POST'])
@login_required
def delete(project_key, repo_id):
    subscription_service.delete(project_key, repo_id)

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
    return redirect(url_for('jira_subscription.index'))
