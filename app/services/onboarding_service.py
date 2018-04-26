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

from os import environ


class OnboardingService(object):
    """A service with the responsibility of handling onboarding logic."""

    def set_trello_organization(self, name):
        """Configures the Trello organization to pull data from."""
        environ['TRELLO_ORG_NAME'] = name

    def set_github_organization(self, login):
        """Configures the GitHub organization to pull data from."""
        environ['GITHUB_ORG_LOGIN'] = login
