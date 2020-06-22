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

"""update_jira_issue_labels.py

Updates a jira issue labels based on GitHub issue data.
"""

import textwrap
from . import GitHubBaseTask
from ..services import JIRAService
from ..models import Issue


class UpdateJiraIssueLabels(GitHubBaseTask):
    """A class that updates the labels of a jira issue in a project."""

    def __init__(self):
        """Initializes a task to update the labels of a jira issue."""
        self._jira_service = JIRAService()

    def run(self, issue_id, project_key, label_names, payload):
        """Performs validations on the event type and enqueues them.

        Validates the event being received is a GitHub Pull Request event or a
        GitHub Issue event, and then enqueues it in the corresponding events
        queue.

        Args:
            issue_id (str): The id of the Github issue.
            project_key (str): The key of the project to raise an issue on.
            label_names (List[str]): A list of label names.
            payload (dict): Github data specific to the JIRA issue to be updated.

        Returns:
            None
        """
        self.payload = payload
        self.set_scope_data()
        issue = Issue.query.filter_by(jira_project_key=project_key, github_issue_id=issue_id).first()
        self._jira_service.update_issue_labels(project_key=project_key, issue_key=issue.jira_issue_key, label_names=label_names)
