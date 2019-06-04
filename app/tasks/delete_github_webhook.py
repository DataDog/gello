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

from celery.task import Task
from ..services import GitHubService
from ..services import RepoService


class DeleteGitHubWebhook(Task):
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

        # Delete a GitHub webhook on given repo
        self._github_service.delete_github_hook(
            webhook_id=webhook_id,
            repo_id=repo_id
        )

        # Reset the webhook_id field to None in repo record in database
        self._delete_webhook_from_database(repo_id=repo_id)

    def _delete_webhook_from_database(self, repo_id):
        """Concrete helper method.

        Internal helper to remove the github_webhook_id field from specified record.

        Args:
            repo_id (int): The id for the repo record to remove webhook id from.

        Returns:
            None
        """
        self._repo_service.remove_webhook(repo_id=repo_id)
