# -*- coding: utf-8 -*-

"""event_receiver.py

Concrete Class representing receiver from GitHub webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from celery.task import Task


class GitHubReceiver(Task):
    """A class that receives webhooks from some the GitHub API."""

    def run(self, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.
        """
        print("Run GitHub receiver task")
        self.payload = payload
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
        pass

    def _create_trello_pull_request_card(self):
        """"""
        pass
