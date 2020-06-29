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

"""onboarding/views.py

onboarding-related routes and view-specific logic.
"""

import textwrap
from os import environ

from flask import redirect, request, url_for, flash, render_template
from flask_login import login_required
from . import onboarding
from .forms import OnboardingForm
from ...services import ConfigValueService, GitHubService, TrelloService, \
    api_services, TrelloMemberService, BoardService, ProjectService, \
    JIRAService
from ...tasks.upsert_github_org_webhook import UpsertGitHubOrgWebhook


github_service = GitHubService()
trello_service = TrelloService()
config_value_service = ConfigValueService()


@onboarding.route('/', methods=['GET', 'POST'])
@login_required
def index():
    onboarding_form = OnboardingForm()

    if onboarding_form.validate_on_submit():
        name = onboarding_form.get_trello_name()
        if name:
            config_value_service.create(key='TRELLO_ORG_NAME', value=name)

        login = onboarding_form.get_github_login()
        config_value_service.create(key='GITHUB_ORG_LOGIN', value=login)

        # Fetch data for the GitHub organization
        for api_service in api_services():
            api_service.fetch()

        # Enqueue a task to create or update a webhook for the org (and persist webhook_id)
        UpsertGitHubOrgWebhook.delay(url_root=request.url_root)

        if name:
            TrelloMemberService().fetch()
            BoardService().fetch()

        jira_address = environ.get('JIRA_SERVER_ADDRESS')

        if jira_address:
            p_serv = ProjectService()
            if p_serv.jira_service.client:
                p_serv.fetch()
            else:
                flash(
                    textwrap.dedent(
                        f"""
                        Could not fetch JIRA information:
                        {p_serv.jira_service.err}
                        """
                    )
                )
                return redirect(url_for('.index'))

        flash(
            textwrap.dedent(
                f"""
                Fetched data for GitHub organization {login}
                """ +
                (', Trello organization ' + name if name else '') +
                (', JIRA server ' + jira_address if jira_address else '')
            )
        )
        if (jira_address):
            return redirect(url_for('jira_subscription.index'))
        else:
            return redirect(url_for('main.index'))

    elif request.method == 'POST':
        flash(
            textwrap.dedent(
                f"""
                Could not continue because an error occurred:
                {onboarding_form.get_error_message()}
                """
            )
        )
        return redirect(url_for('.index'))

    github_organizations = github_service.organizations()
    trello_organizations = trello_service.organizations()

    return render_template(
        'onboarding.html',
        onboarding_form=onboarding_form,
        github_organizations=github_organizations,
        trello_organizations=trello_organizations
    )
