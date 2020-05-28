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
from . import subscribed_item
from .forms import NewForm, UpdateForm, DeleteForm
from ...services import SubscribedJIRAItemService
from ...models import Subscription, SubscribedJIRAIssue, JIRAMember, \
    JIRAIssueType, ConfigValue

subscribed_item_service = SubscribedJIRAItemService()


@subscribed_item.route(
    '/<string:project_key>/<int:repo_id>',
    methods=['GET', 'POST']
)
@login_required
def index(project_key, repo_id):
    """
    Displays JIRA projects/issues pertaining to a particular subscription.
    """
    if not ConfigValue.get_or_insert_jira_address():
        return render_template(
            '500.html',
            jira_description="No JIRA server found, please set JIRA config values"
        ), 500

    # Creation form logic
    create_form = NewForm(project_key, repo_id)
    if create_form.validate_on_submit():
        member_id = create_form.get_jira_member_id()

        if not isinstance(member_id, list):
            subscribed_item_service.create(
                project_key=project_key,
                repo_id=repo_id,
                issue_type_id=create_form.get_issue_type(),
                jira_issue_key=create_form.get_issue_key(),
                jira_member_id=member_id
            )

        flash('Created subscription')
        return redirect(url_for('.index', project_key=project_key, repo_id=repo_id))
    elif request.method == 'POST':
        flash(
            textwrap.dedent(
                f"""
                Could not create subscribed list because an error occurred:
                {create_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index', project_key=project_key, repo_id=repo_id))

    sub_id = Subscription.query.filter_by(
        project_key=project_key, repo_id=repo_id
    ).first()
    sub_id = 0 if not bool(sub_id) else sub_id.id

    subscription = Subscription.query.get_or_404([sub_id, repo_id])
    issues = subscription.subscribed_jira_issues.order_by(
        SubscribedJIRAIssue.timestamp.asc()
    )

    issue_form_pairs = []

    project_sub = subscription.subscribed_jira_projects
    if project_sub.count():
        proj = project_sub[0]
        member = JIRAMember.query.filter_by(
            jira_member_id=proj.jira_member_id).first()

        if member:
            update_form = UpdateForm(jira_update_id=member.jira_member_id)
        else:
            update_form = UpdateForm()

        issue_form_pairs.append((proj, update_form, DeleteForm(), False,
                                 JIRAIssueType.query.filter_by(
                                    issue_type_id=proj.issue_type_id
                                ).first().name,
                                 member.name if member else None))

    for iss in issues:
        member = JIRAMember.query.filter_by(
            jira_member_id=iss.jira_member_id).first()

        if member:
            update_form = UpdateForm(jira_update_id=member.jira_member_id)
        else:
            update_form = UpdateForm()

        issue_form_pairs.append((iss, update_form, DeleteForm(), True, None,
                                 member.name if member else None))

    return render_template(
        'subscribed_jira_items.html',
        create_form=create_form,
        subscription=subscription,
        issue_form_pairs=issue_form_pairs
    )


@subscribed_item.route(
    '/<string:project_key>/<int:repo_id>/update/<string:issue_key>',
    methods=['POST']
)
@login_required
def update(project_key, repo_id, issue_key):
    if issue_key == '0':
        issue_key = None
    update_form = UpdateForm(request.form)

    if update_form.validate():
        member_id = update_form.get_jira_member_id()

        subscribed_item_service.update(
            project_key=project_key,
            repo_id=repo_id,
            jira_issue_key=issue_key,
            jira_member_id=member_id
        )

        flash('Updated subscription')
        return redirect(url_for('.index', project_key=project_key, repo_id=repo_id))
    else:
        flash(
            textwrap.dedent(
                f"""
                Could not update subscribed item because an error occurred:
                {update_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index', project_key=project_key, repo_id=repo_id))


@subscribed_item.route(
    '/<string:project_key>/<int:repo_id>/delete/<string:issue_key>',
    methods=['POST']
)
@login_required
def delete(project_key, repo_id, issue_key):
    if issue_key == '0':
        issue_key = None
    subscribed_item_service.delete(project_key, repo_id, issue_key)
    flash('Deleted subscription')
    return redirect(url_for('.index', project_key=project_key, repo_id=repo_id))
