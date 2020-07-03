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

"""delete_github_webhook.py

Deletes a webhook from a repository.
"""

from .db_task import DBTask
from ..services import GitHubService
from ..services import RepoService


class DeleteGitHubWebhook(DBTask):
    """A task to delete an existing GitHub Webhook."""

    def __init__(self):
        """Initializes a `GitHubService` object for the class."""
        self._github_service = GitHubService()
        self._repo_service = RepoService()

    def run(self, webhook_id, repo_id):
        """Deletes a GitHub webhook from a repository.

        Args:
            webhook_id (int): The id for the webhook to be deleted.
            repo_id (int): The id of the repository to delete the webhook from.

        Returns:
            None
        """
        self._github_service.delete_github_hook(webhook_id=webhook_id, repo_id=repo_id)

        # Reset the webhook_id field to None in repo record in database
        self._repo_service.remove_webhook(repo_id=repo_id)
