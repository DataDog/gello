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

"""delete_jira_issue.py

Deletes a JIRA issue object.
"""

from . import GitHubBaseTask
from ..services import IssueService, PullRequestService


class DeleteJIRAIssueObjectFromDatabase(GitHubBaseTask):
    """A class that deletes a JIRA Issue object within Gello."""

    def __init__(self):
        """Initializes a task to create a manual trello card."""
        self._issue_service = IssueService()
        self._pull_request_service = PullRequestService()

    def run(self, scope, github_id):
        """Deletes the record of the JIRA issue in Gello.

        NOTE: this does not delete the card on JIRA, only removes
        the record from the database in Gello.

        Args:
            scope (str): The scope of the webhook payload (i.e., `issue`, or
                `pull_request`).
            github_id (int): The GitHub id of the record to be deleted.

        Returns:
            None
        """
        if scope == 'issue':
            self._issue_service.delete(github_issue_id=github_id)
        elif scope == 'pull_request':
            self._pull_request_service.delete(github_pull_request_id=github_id)
        else:
            print('Unsupported GitHub scope')
