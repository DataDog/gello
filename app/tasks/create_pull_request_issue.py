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

"""create_pull_request_issue.py

Creates a JIRA issue based on GitHub pull request data.
"""

import textwrap
from . import CreateJIRAIssue
from ..services import PullRequestService


class CreatePullRequestIssue(CreateJIRAIssue):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create a pull request trello card."""
        super().__init__()
        self._pull_request_service = PullRequestService()

    def _issue_body(self):
        """Concrete helper method.

        Internal helper to format the jira issue description, based on the data
        passed in.

        Returns:
            str: the markdown template for the JIRA Issue created.
        """
        return textwrap.dedent(
            f"""
            # GitHub Pull Request Opened By Community Member
            ---
            - Pull Request link: [{self._title}]({self._url})
            - Opened by: [{self._user}]({self._user_url})
            ---
            ### Pull Request Body
            ---
            """
        ) + self._body

    def _persist_issue_to_database(self, issue):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            issue (trello.Issue): An object representing the JIRA created.

        Returns:
            None
        """
        self._pull_request_service.create(
            name=self._title,
            url=self._url,
            github_pull_request_id=self._id,
            repo_id=self._repo_id,
            jira_project_key=issue.jira_project_key,
            jira_issue_id=issue.jira_issue_id,
            jira_issue_url=issue.jira_issue_url,
            jira_parent_issue_id=issue.jira_parent_issue_id
        )
