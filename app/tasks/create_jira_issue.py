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

"""create_jira_issue.py

Creates a JIRA issue on a specific project board
"""

from jira import JIRAError

from . import GitHubBaseTask
from ..services import JIRAService


class CreateJIRAIssue(GitHubBaseTask):
    """An abstract class responsible for creating an issue on a JIRA project
    board"""

    def __init__(self):
        """Initializes a task to create a JIRA issue"""

        self._jira_service = JIRAService()
        pass

    def run(self, project_key, issue_type, payload, parent_issue=None,
            assignee_id=None, label_name=None):
        """Enqueues a JIRA creation event

        Args:
            project_key (str): The key of the project to raise an issue on
            issue_type (str): The id of the issue type of the project
            payload (dict): Data specific to the JIRA issue to be created
                summary (str): A summary of the issue
                description (str): A description of the issue
            parent_issue (str): The key of the parent issue for this sub-issue
            label_name (str): The name of the auto-generated label
            asignee_id (str): id of the user the new issue will be assigned to

        Returns:
            None
        """

        self.payload = payload
        self.set_scope_data()
        self._repo_id = self.payload['repository']['id']

        try:
            # Create a JIRA issue on a given project
            issue = self.jira_service().create_issue(
                project_key=project_key,
                issue_type=issue_type,
                summary=self._title,
                description=self._issue_body(),
                parent_issue=parent_issue,
                assignee_id=assignee_id,
                label_name=label_name
            )

            # Persist the new JIRA issue to the database
            self._persist_issue_to_database(issue=issue)

        except JIRAError as err:
            print(err)
            return err

    def jira_service(self):
        """Returns the JiraService instance.

        Returns:
            JiraService
        """
        return self._jira_service

    def _issue_body(self):
        """Abstract helper method.

        Internal helper to format the JIRA issue body, based on the data
        passed in.
        """
        pass

    def persist_issue_to_database(self, issue):
        """Abstract helper method.

        Internal helper to save the record created to the database.
        """
        pass
