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

"""create_manual_issue.py

Creates a JIRA issue based on GitHub manual data.
"""

import textwrap
from . import CreateJIRAIssue
from ..services import IssueService, PullRequestService


class CreateManualIssue(CreateJIRAIssue):
    """A class that creates a JIRA issue on a board."""

    def __init__(self):
        """Initializes a task to create a manual JIRA issue."""
        super().__init__()
        self._issue_service = IssueService()
        self._pull_request_service = PullRequestService()

    def _card_body(self):
        """Concrete helper method.

        Internal helper to format the JIRA issue body, based on the data
        passed in.

        Returns:
            str: the markdown template for the JIRA issue created.
        """
        return textwrap.dedent(
            f"""
            h1. GitHub JIRA Issue Opened By Organization Member
            ----

            * Link: [{self._title}|{self._url}]
            * Opened by: [{self._user}|{self._user_url}]
            ----

            h3. {self.get_scope().capitalize()} Body
            ----

            """
        ) + self._body

    def _persist_issue_to_database(self, issue):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            issue (jira.Issue): an object representing the JIRA issue created

        Returns:
            None
        """
        scope = self.get_scope()

        if scope == 'issue':
            self._issue_service.create(
                name=self._title,
                url=self._url,
                github_issue_id=self._id,
                repo_id=self._repo_id,
                jira_project_key=issue.fields.project.key,
                jira_issue_key=issue.key,
                jira_parent_issue_key=issue.fields.parent.key
                if hasattr(issue.fields, 'parent') else None
            )
        elif scope == 'pull_request':
            self._pull_request_service.create(
                name=self._title,
                url=self._url,
                github_pull_request_id=self._id,
                repo_id=self._repo_id,
                jira_project_key=issue.fields.project.key,
                jira_issue_key=issue.key,
                jira_parent_issue_key=issue.fields.parent.key
                if hasattr(issue.fields, 'parent') else None
            )
        else:
            print('Unsupported GitHub scope')
