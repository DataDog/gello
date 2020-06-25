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

"""upsert_github_org_webhook.py

Updates or creates a webhook for an organization.
"""

from os import environ

from celery.task import Task
from ..models import ConfigValue
from ..services.github_service import GitHubService
from ..services.environment_variable_service import EnvironmentVariableService


class UpsertGitHubOrgWebhook(Task):
    """A task to update or create a GitHub Organization Webhook."""

    def __init__(self):
        """Initializes a `UpsertGitHubOrgWebhook` object for the class."""
        pass

    def run(self, url_root):
        """Updates or creates a GitHub webhook for an organization.

        Args:
            url_root (str): The url for Gello webhooks to be received.

        Returns:
            None
        """
        self._environment_variable_service = EnvironmentVariableService()
        self._environment_variable_service.export_persisted_variables()
        self._github_service = GitHubService()

        existing_hook = self._github_service.get_org_webhook(url_root=url_root)

        if existing_hook:
            if 'organization' not in existing_hook.events:
                self._github_service.update_webhook_events(existing_hook, ['organization'])
            self._github_service.upsert_webhook(webhook_id=existing_hook.id)
        else:
            webhook_id = self._github_service.create_github_org_hook(url_root=url_root)
            self._github_service.upsert_webhook(webhook_id=webhook_id)
