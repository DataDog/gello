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

from os import environ
import textwrap

from flask import redirect, request, url_for, flash, render_template
from flask_login import login_required
from . import onboarding
from .forms import OnboardingForm
from ...services import OnboardingService, GitHubService, TrelloService, \
    api_services

github_service = GitHubService()
trello_service = TrelloService()
onboarding_service = OnboardingService()


@onboarding.route('/', methods=['GET', 'POST'])
@login_required
def index():
    onboarding_form = OnboardingForm()

    if onboarding_form.validate_on_submit():
        name = onboarding_form.get_trello_name()
        onboarding_service.set_trello_organization(name=name)

        login = onboarding_form.get_github_login()
        onboarding_service.set_github_organization(login=login)

        # Fetch data for the GitHub and Trello organizations
        for api_service in api_services():
            api_service.fetch()

        # Persist new environment variables for the next time the server is run
        onboarding_service.write_out_environment_variables()

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
