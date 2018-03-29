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


class CreateGitHubWebhook(Task):
    """A task to create a GitHub Webhook."""

    def __init__(self):
        self._github_service = GitHubService()

    def run(self, url_root, repo_id):
        """Creates a GitHub webhook for a repository."""
        self._github_service.create_github_hook(
            url_root=url_root,
            repo_id=repo_id
        )
