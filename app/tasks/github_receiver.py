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

"""github_receiver.py

Concrete Class representing receiver from GitHub webhooks. Each receiver is a
celery task, which is enqueued in the receivers task queue.
"""

from . import GitHubBaseTask
from . import CreateIssueCard, CreatePullRequestCard, CreateManualCard, \
    DeleteTrelloCard
from ..models import Subscription, Contributor, Repo, Board, Issue, PullRequest


class GitHubReceiver(GitHubBaseTask):
    """A class that receives webhooks from some the GitHub API."""

    def run(self, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.
        """
        print('Run GitHub receiver task.')
        self.payload = payload
        self._enqueue_task()

    def _user_in_organization(self):
        """Checks if the person is in the organization.

        Returns:
            Boolean: `true` if the user belongs to the organization
        """
        contributor = Contributor.query.filter_by(
            member_id=self.payload['sender']['id']
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
                    list_id=trello_list.trello_list_id,
                    autocard=subscription.autocard
                )

    def _create_card(self, board_id, list_id, autocard):
        """Determines which type of card to create based on the payload."""
        scope = self.get_scope()
        action = self.payload['action']

        if not autocard and 'comment' in self.payload and action == 'created' and \
           self._manual_command_string() in self.payload['comment']['body']:
            self._create_manual_card(board_id, list_id)
        elif autocard and scope == 'issue' and action == 'opened':
            self._create_trello_issue_card(board_id, list_id)
        elif autocard and scope == 'pull_request' and action == 'opened':
            self._create_trello_pull_request_card(board_id, list_id)
        elif scope == 'issue' and action == 'closed':
            self._delete_issue_trello_cards()
        elif scope == 'pull_request' and action == 'closed':
            self._delete_pull_request_trello_cards()
        else:
            print('Unsupported event action.')

    def _create_manual_card(self, board_id, list_id):
        """Creates a task to create a trello card."""
        # Don't create a card if the user DOES NOT belong to the organization
        if not self._user_in_organization():
            print('The user does not belong to the organization.')
            return

        CreateManualCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=f"Manual card created by {self.payload['sender']['login']}",
            payload=self.payload
        )

    def _create_trello_issue_card(self, board_id, list_id):
        """Creates a task to create a trello card."""
        # Don't create a card if the user belongs to the organization
        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreateIssueCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['issue']['title'],
            payload=self.payload
        )

    def _create_trello_pull_request_card(self, board_id, list_id):
        """Creates a task to create a trello card."""
        # Don't create a card if the user belongs to the organization
        if self._user_in_organization():
            print('The user belongs to the organization, not creating card.')
            return

        CreatePullRequestCard.delay(
            board_id=board_id,
            list_id=list_id,
            name=self.payload['pull_request']['title'],
            payload=self.payload
        )

    def _delete_issue_trello_cards(self):
        """Deletes all trello cards associated with an issue."""
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        issues = Issue.query.filter_by(github_issue_id=github_id)

        for issue in issues:
            DeleteTrelloCard.delay(
                scope=scope,
                github_id=github_id,
                card_id=issue.trello_card_id
            )

    def _delete_pull_request_trello_cards(self):
        """Deletes all trello cards associated with a pull request."""
        scope = self.get_scope()
        github_id = self.payload[scope]['id']
        pull_requests = PullRequest.query.filter_by(
            github_pull_request_id=github_id)

        for pull_request in pull_requests:
            DeleteTrelloCard.delay(
                scope=scope,
                github_id=github_id,
                card_id=pull_request.trello_card_id
            )

    def _manual_command_string(self):
        """The command to create a card when `autocard` is disabled."""
        return 'gello create_card'
