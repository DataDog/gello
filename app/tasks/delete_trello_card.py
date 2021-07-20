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

Deletes a trello card object.
"""

from . import GitHubBaseTask
from ..services import IssueService, PullRequestService


class DeleteCardObjectFromDatabase(GitHubBaseTask):
    """A class that deletes a trello card object within Gello."""

    def __init__(self):
        """Initializes a task to create a manual trello card."""
        self._issue_service = IssueService()
        self._pull_request_service = PullRequestService()

    def run(self, scope, github_id, db_id=None):
        """Deletes the record of the trello card in Gello.

        NOTE: this does not delete the card on the Trello board, only removes
        the record from the database in Gello.

        Args:
            scope (str): The scope of the webhook payload (i.e., `issue`, or
                `pull_request`).
            github_id (int): The GitHub id of the record to be deleted.

        Returns:
            None
        """
        if scope == 'issue':
            if db_id:
                self._issue_service.delete_by_id(issue_id=db_id)
            else:
                self._issue_service.delete(github_issue_id=github_id)
        elif scope == 'pull_request':
            if db_id:
                self._pull_request_service.delete_by_id(pull_request_id=db_id)
            else:
                self._pull_request_service.delete(github_pull_request_id=github_id)
        else:
            print('Unsupported GitHub scope')
