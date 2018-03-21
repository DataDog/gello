# -*- coding: utf-8 -*-

"""Concrete Class representing receiver from GitHub webhooks

Each receiver is a celery task, which is enqueued in the receivers task queue.
"""

from gello.event_receiver.event_receiver import EventReceiver
from gello.event_actions.create_trello_card import CreateTrelloCard


class GitHubReceiver(EventReceiver):
    """A class that receives webhooks from some the GitHub API."""

    def __init__(self, payload):
        """Initializes a new GitHubReceiver object."""
        self.payload = payload
        super(self)

    def run(self):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.
        """
        self._enqueue_task()

    def _enqueue_task(self):
        """Enqueues a EventAction task based on the payload parameters."""
        if self.payload["issue"]:
            self._create_trello_issue_card()
        elif self.payload["pull_request"]:
            self._create_trello_pull_request_card()
        else:
            raise ValueError('Unsupported event action.')

    def _create_trello_issue_card(self):
        """"""
        CreateTrelloCard.s(
            name=self.payload["issue"]["title"],
            url=self.payload["issue"]["url"]
        ).apply_async(queue='trello.issues')

    def _create_trello_pull_request_card(self):
        """"""
        CreateTrelloCard.s(
            name=self.payload["issue"]["title"],
            url=self.payload["issue"]["url"]
        ).apply_async(queue='trello.pull_requests')
