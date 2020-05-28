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

"""jira_service.py

Service-helpers for interacting with the Jira API.
"""

from ..api_clients import JIRAAPIClient


class JIRAService(object):
    """
    A class providing an interface with the Jira API client.
    """

    def __init__(self):
        """
        Initializes a new JiraService object
        """
        self._client_wrapper = JIRAAPIClient()
        self.client = self._client_wrapper.client()
        self.err = self._client_wrapper.err

    def _init_if_needed(self):
        if not self.client:
            self._client_wrapper.initialize()
            self.client = self._client_wrapper.client()
            self.err = self._client_wrapper.err
        return bool(self.client)

    def projects(self):
        """
        Returns a list of tuples (project key, project name)
        """
        if self._init_if_needed():
            return self.client.projects()

    def members(self):
        """
        Returns a list of members of the organization
        """
        if self._init_if_needed():
            return self.client.search_users(query='')

    def get_issue_types(self, project_key):
        """
        Returns a list of issue types for a given project key
        """
        if self._init_if_needed():
            return self.client.project(project_key).issueTypes

    def get_project_issues(self, project_key):
        """
        Returns a list of issue objects for a given project
        """
        if self._init_if_needed():
            return self.client.search_issues(
                'project = "' + project_key +
                '" AND issuetype not in subtaskIssueTypes() AND' +
                ' resolution = Unresolved'
            )

    def get_project_members(self, project_key):
        """
        Returns a list of assignable jira member objects for a given project
        """
        if self._init_if_needed():
            return self.client.search_assignable_users_for_projects(
                '', project_key)

    def create_issue(self, project_key, summary, description, issue_type=None,
                     parent_issue=None, assignee_id=None, label_name=None):
        """
        Creates a new issue of type issue_type under the project with 
        project_key populated with the provided fields

        Args:
            project_key (str): The key of the project to raise an issue on
            summary (str): A summary of the issue
            description (str): A description of the issue
            issue_type (str): The id of the issue type of the project
                (optional)
            parent_issue (str): The key of the parent issue for this sub-issue
                (optional)
            assignee_id (str): id of the user the new issue will be assigned to
                (optional)
            label_id (str): The id of the repo-specific language label.
                (optional)

        Returns:
            jira.issue: object representing a JIRA issue
        """
        if self._init_if_needed():
            return self.client.create_issue(
                summary=summary,
                parent=(None, {"key": parent_issue})[bool(parent_issue)],
                issuetype=({"id": issue_type},
                           {"name": issue_type})[bool(parent_issue)],
                project={"key": project_key},
                description=description,
                assignee=(None, {"accountId": assignee_id})[bool(assignee_id)],
                labels=(None, [label_name])[bool(label_name)]
            )
