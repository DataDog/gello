# -*- coding: utf-8 -*-

"""github_receiver.py

Concrete Class representing receiver from GitHub webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from celery.task import Task
from . import CreateIssueCard, CreatePullRequestCard
# from .. import db
from ..models import Board, Repo


class GitHubReceiver(Task):
    """A class that receives webhooks from some the GitHub API."""

    def run(self, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.
        """
        print('Run GitHub receiver task')
        self.payload = payload
        self._enqueue_task()

    def _enqueue_task(self):
        """Enqueues a EventAction task based on the payload parameters."""
        # if invalid repository, early return
        repo = Repo.query.filter_by(
            github_repo_id=self.payload['repository']['id']).first()

        # The repository must exist
        if repo is None:
            return

        board = Board.query.filter_by(trello_board_id=repo.board_id).first()

        # The repository must belong to a board
        if board is None:
            return

        if self.payload['issue']:
            self._create_trello_issue_card(repo.board_id, board.list_id)
        elif self.payload['pull_request']:
            self._create_trello_pull_request_card(repo.board_id, board.list_id)
        else:
            raise ValueError('Unsupported event action.')

    def _create_trello_issue_card(self, board_id, list_id):
        """Creates a task to create a trello card."""
        CreateIssueCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['issue']['title'],
            metadata=self.payload
        )

    def _create_trello_pull_request_card(self, board_id, list_id):
        """Creates a task to create a trello card."""
        CreatePullRequestCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['issue']['title'],
            metadata=self.payload
        )
