# -*- coding: utf-8 -*-

"""__init__.py

Task-specific initialization code.
"""

from .. import celery

from .create_trello_card import CreateTrelloCard
from .create_issue_card import CreateIssueCard
from .create_pull_request_card import CreatePullRequestCard
from .event_receiver import GitHubReceiver


def _register_tasks():
    """Registers class based celery tasks with celery worker"""
    celery.tasks.register(CreateTrelloCard())
    celery.tasks.register(CreateIssueCard())
    celery.tasks.register(CreatePullRequestCard())
    celery.tasks.register(GitHubReceiver())


_register_tasks()
