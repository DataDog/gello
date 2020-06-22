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

"""create_github_webhook.py

Creates a webhook for a repository.
"""

from celery.task import Task
from ..services import GitHubService
from ..services import RepoService


class CreateGitHubWebhook(Task):
    """A task to create a GitHub Repo Webhook."""

    def __init__(self):
        """Initializes a `GitHubService` object for the class."""
        self._github_service = GitHubService()
        self._repo_service = RepoService()

    def run(self, url_root, repo_id):
        """Creates a GitHub webhook for a repository.

        Args:
            url_root (str): The url for Gello webhooks to be received.
            repo_id (int): The id of the repository to create the webhook to.

        Returns:
            None
        """

        # Create a GitHub webhook on given repo
        webhook_id = self._github_service.create_github_hook(url_root=url_root, repo_id=repo_id)

        # Persist the webhook_id field to repo record in database
        self._repo_service.add_webhook(webhook_id=webhook_id, repo_id=repo_id)
