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

"""update_jira_pull_request_issue_labels.py

Updates a jira issue labels based on GitHub pull request data.
"""

from . import GitHubBaseTask
from ..services import JIRAService
from ..models import PullRequest


class AppendJiraPullRequestIssueLabels(GitHubBaseTask):
    """A class that updates the labels of a jira issue in a project."""

    def __init__(self):
        """Initializes a task to update the labels of a jira issue."""
        self._jira_service = JIRAService()

    def run(self, jira_issue_key, project_key, label_names, payload):
        """Call the JIRA client to append lables to the issue

        Args:
            jira_issue_key (str): The key of the JIRA issue to update.
            project_key (str): The key of the project to raise an issue on.
            label_names (List[str]): A list of label names.
            payload (dict): Github data specific to the JIRA issue to be updated.

        Returns:
            None
        """
        self.payload = payload
        self.set_scope_data()
        self._jira_service.append_issue_labels(project_key=project_key, issue_key=jira_issue_key, label_names=label_names)
