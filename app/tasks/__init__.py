# -*- coding: utf-8 -*-

"""__init__.py

Task-specific initialization code.
"""

from .. import celery

from .create_trello_card import CreateTrelloCard
from .event_receiver import GitHubReceiver


def _register_tasks():
    """Registers class based celery tasks with celery worker"""
    celery.tasks.register(CreateTrelloCard())
    celery.tasks.register(GitHubReceiver())


_register_tasks()
