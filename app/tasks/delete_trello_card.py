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

"""delete_trello_card.py

Deletes a trello card.
"""

from . import GitHubBaseTask
from ..services import IssueService, PullRequestService, TrelloService


class DeleteTrelloCard(GitHubBaseTask):
    """A class that deletes a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a manual trello card."""
        self._issue_service = IssueService()
        self._pull_request_service = PullRequestService()
        self._trello_service = TrelloService()

    def run(self, scope, github_id, card_id):
        """Deletes a trello card trello card."""
        # Deletes the card on the trello board
        self._trello_service.delete_card(card_id=card_id)

        # Deletes the card record in the database
        if scope == 'issue':
            self._issue_service.delete(github_issue_id=github_id)
        elif scope == 'pull_request':
            self._pull_request_service.delete(github_pull_request_id=github_id)
        else:
            print('Unsupported GitHub scope')
