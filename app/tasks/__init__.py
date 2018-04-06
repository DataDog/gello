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

"""__init__.py

Task-specific initialization code.
"""

from .. import celery

from .github_base_task import GitHubBaseTask
from .delete_trello_card import DeleteCardObjectFromDatabase
from .create_github_webhook import CreateGitHubWebhook
from .create_trello_card import CreateTrelloCard
from .create_issue_card import CreateIssueCard
from .create_pull_request_card import CreatePullRequestCard
from .create_manual_card import CreateManualCard
from .github_receiver import GitHubReceiver


def _register_tasks():
    """Registers class based celery tasks with celery worker"""
    celery.tasks.register(GitHubBaseTask())
    celery.tasks.register(DeleteCardObjectFromDatabase())
    celery.tasks.register(CreateTrelloCard())
    celery.tasks.register(CreateIssueCard())
    celery.tasks.register(CreateManualCard())
    celery.tasks.register(CreatePullRequestCard())
    celery.tasks.register(CreateGitHubWebhook())
    celery.tasks.register(GitHubReceiver())


_register_tasks()
