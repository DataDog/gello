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

from flask import redirect, request, url_for, flash, render_template
from flask_login import login_required
from . import onboarding
from .forms import OnboardingForm
from ...services import ConfigValueService, GitHubService, TrelloService, \
    api_services

github_service = GitHubService()
trello_service = TrelloService()
config_value_service = ConfigValueService()


@onboarding.route('/', methods=['GET', 'POST'])
@login_required
def index():
    onboarding_form = OnboardingForm()

    if onboarding_form.validate_on_submit():
        name = onboarding_form.get_trello_name()
        config_value_service.create(key='TRELLO_ORG_NAME', value=name)

        login = onboarding_form.get_github_login()
        config_value_service.create(key='GITHUB_ORG_LOGIN', value=login)

        # Fetch data for the GitHub and Trello organizations
        for api_service in api_services():
            api_service.fetch()

        flash(
            textwrap.dedent(
                f"""
                Fetched data for Trello organization {name} and GitHub
                organization {login}
                """
            )
        )

        return redirect(url_for('.index'))
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
