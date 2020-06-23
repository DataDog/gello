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

"""create_github_org_webhook.py

Creates a webhook for an organization.
"""

from os import environ

from celery.task import Task
from ..services.github_service import GitHubService
from ..services.github_member_service import GitHubMemberService
from ..services.environment_variable_service import EnvironmentVariableService


class CreateGitHubOrgWebhook(Task):
    """A task to create a GitHub Organization Webhook."""

    def __init__(self):
        """Initializes a `CreateGitHubOrgWebhook` object for the class."""
        pass

    def run(self, url_root):
        """Creates a GitHub webhook for an organization.

        Args:
            url_root (str): The url for Gello webhooks to be received.

        Returns:
            None
        """
        self._environment_variable_service = EnvironmentVariableService()
        self._environment_variable_service.export_persisted_variables()
        self._github_service = GitHubService()
        self._github_member_service = GitHubMemberService()

        webhook_id = self._github_service.create_github_org_hook(url_root=url_root)
        self._github_member_service.add_webhook(webhook_id=webhook_id)
