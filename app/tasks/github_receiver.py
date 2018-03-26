# -*- coding: utf-8 -*-

"""github_receiver.py

Concrete Class representing receiver from GitHub webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from celery.task import Task
from . import CreateIssueCard, CreatePullRequestCard
from ..models import Subscription, Contributor, Repo, Board


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

        # Don't create a card if the user belongs to the organization
        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        self._enqueue_task()

    def _user_in_organization(self):
        """Checks if the person is in the organization.

        Returns:
            Boolean: `true` if the user belongs to the organization
        """
        contributor = Contributor.query.filter_by(
            member_id=self.payload['issue']['user']['id']
        ).first()

        return contributor is not None

    def _enqueue_task(self):
        """Enqueues a EventAction task based on the payload parameters."""
        repo = Repo.query.filter_by(
            github_repo_id=self.payload['repository']['id']
        ).first()

        # The repository must exist
        if repo is None:
            print('The repository does not exist in the database.')
            return

        # Get all of the subscriptions related to a repository
        subscriptions = Subscription.query.filter_by(repo_id=repo.github_repo_id)

        for subscription in subscriptions:
            # TODO: research a better query for this
            trello_lists = Board.query.filter_by(
                trello_board_id=subscription.board_id).first().lists

            # Only create a card on an active list
            active_lists = filter(lambda s: s.active, trello_lists)

            for trello_list in active_lists:
                self._create_card(
                    board_id=subscription.board_id,
                    list_id=trello_list.trello_list_id
                )

    def _create_card(self, board_id, list_id):
        """Determines which type of card to create based on the payload."""
        if self.payload['issue']:
            self._create_trello_issue_card(board_id, list_id)
        elif self.payload['pull_request']:
            self._create_trello_pull_request_card(board_id, list_id)
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
