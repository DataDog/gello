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

"""subscriptions/forms.py

Subscription-related forms.
"""

import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from app.services import GitHubService, TrelloService


class OnboardingForm(FlaskForm):
    """Form for creating a new subscription."""
    github_organization_login = StringField(
        'GitHub Organization Login',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The login for the GitHub organization you wish to pull repositories
            and members from
            """
        )
    )
    trello_organization_name = StringField(
        'Trello Organization Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name for the Trello organization you wish to pull boards,
            lists, and members from
            """
        )
    )
    submit = SubmitField('Done')

    def __init__(self):
        self.github_service = GitHubService()
        self.trello_service = TrelloService()
        super().__init__()

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `trello_organization_name` attribute corresponds to a
          Trello organization accessible with the trello credentials
        - Validates the `github_organization_login` attribute corresponds to a
          GitHub organization accessible with the api token
        """
        trello_organization_name = self.trello_organization_name.data.strip()
        github_organization_login = self.github_organization_login.data.strip()

        # Check that the Trello organization name exists
        trello_organizations = self.trello_service.organizations()
        trello_organization_names = [o.name for o in trello_organizations]

        if trello_organization_name not in trello_organization_names:
            self._error_message = textwrap.dedent(
                f"""
                The Trello organization is not accessible with the provided
                TRELLO_API_KEY and TRELLO_API_TOKEN
                """
            )
            return False

        self._trello_name = trello_organization_name

        # Check that the GitHub organization login exists
        github_organizations = self.github_service.organizations()
        github_organization_logins = [o.login for o in github_organizations]

        if github_organization_login not in github_organization_logins:
            self._error_message = textwrap.dedent(
                f"""
                The GitHub organization is not accessible with the provided
                GITHUB_API_TOKEN
                """
            )
            return False

        self._github_login = github_organization_login

        # All custom validations passed
        return True

    def get_trello_name(self):
        return self._trello_name

    def get_github_login(self):
        return self._github_login

    def get_error_message(self):
        return self._error_message
