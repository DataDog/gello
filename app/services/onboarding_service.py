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

"""OnboardingService"""

import textwrap
from os import environ, path
from flask import current_app


class OnboardingService(object):
    """A service with the responsibility of handling onboarding logic."""

    def set_trello_organization(self, name):
        """Configures the Trello organization to pull data from."""
        environ['TRELLO_ORG_NAME'] = name

    def set_github_organization(self, login):
        """Configures the GitHub organization to pull data from."""
        environ['GITHUB_ORG_LOGIN'] = login

    def write_out_environment_variables(self):
        """Writes out all the environment variables to a file."""
        env_file_path = path.join(current_app.root_path, '../', '.env')
        with open(env_file_path, 'w+') as env_file:
            env_file.write(
                textwrap.dedent(
                    f"""
                    # Admin user configuration
                    ADMIN_EMAIL='{environ.get('ADMIN_EMAIL')}'
                    ADMIN_PASSWORD='{environ.get('ADMIN_PASSWORD')}'

                    # Database configuration
                    DATABASE_URL='{environ.get('DATABASE_URL')}'

                    # GitHub configuration values
                    GITHUB_API_TOKEN='{environ.get('GITHUB_API_TOKEN')}'
                    GITHUB_ORG_LOGIN='{environ.get('GITHUB_ORG_LOGIN')}'

                    # Trello configuration values
                    TRELLO_ORG_NAME='{environ.get('TRELLO_ORG_NAME')}'
                    TRELLO_API_KEY='{environ.get('TRELLO_API_KEY')}'
                    TRELLO_API_TOKEN='{environ.get('TRELLO_API_TOKEN')}'
                    """
                )
            )
