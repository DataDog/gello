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

"""issue_service.py

Service-helpers for creating and mutating issue data.
"""

from . import CRUDService
from .. import db
from ..models import Issue


class IssueService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating Issue
    data.
    """

    def create(self, name, url, github_issue_id, repo_id, trello_board_id=None,
               trello_card_id=None, trello_card_url=None, trello_list_id=None,
               jira_issue_key=None, jira_project_key=None,
               jira_parent_issue_key=None):
        """Creates and persists a new issue record to the database.

        Args:
            name (str): The name of the GitHub issue.
            url (str): The GitHub url of the issue.
            github_issue_id (int): The id of the GitHub issue.
            repo_id (int): The id of the GitHub repo corresponding to the
                issue.
            trello_board_id (str): The id of the board the card corresponding
                to the issue was created on.
            trello_card_id (str): The id of the card created corresponding to
                the isuse.
            trello_card_url (str): The url for the created card corresponding
                to the issue.
            trello_list_id (str): The id for the list the card corresponding
                to the issue was created on.
            jira_issue_key (str): The key of the created jira issue
                corresponding to the github issue
            jira_project_key (str): The key of the project the jira issue
                corresponding to the github issue was created under
            jira_parent_issue_key (str): The key of the jira issue the
                sub-issue corresponding to the github issue was created under
                (if a jira sub-issue was indeed created)

        Returns:
            None
        """

        issue = Issue(
            name=name,
            url=url,
            github_issue_id=github_issue_id,
            repo_id=repo_id,
            trello_board_id=trello_board_id,
            trello_card_id=trello_card_id,
            trello_card_url=trello_card_url,
            trello_list_id=trello_list_id,
            jira_issue_key=jira_issue_key,
            jira_project_key=jira_project_key,
            jira_parent_issue_key=jira_parent_issue_key
        )
        db.session.add(issue)

        # Persists the issue
        db.session.commit()

    def update(self, github_issue_id, name):
        """Updates a persisted issue.

        Args:
            github_issue_id (int): The id of the GitHub issue.
            name (str): The updated name of the GitHub issue.

        Returns:
            None
        """

        for iss in Issue.query.filter_by(
            github_issue_id=github_issue_id
        ):
            iss.name = name
        db.session.commit()

    def delete(self, github_issue_id):
        """Deletes an old, persisted issue.

        Args:
            github_issue_id (int): The id of the GitHub issue.

        Returns:
            None
        """
        Issue.query.filter_by(github_issue_id=github_issue_id).delete()
        db.session.commit()

    def delete_by_id(self, issue_id):
        """Deletes an old, persisted issue by id.

        Args:
            issue_id (int): The db id of the issue.

        Returns:
            None
        """
        Issue.query.filter_by(id=issue_id).delete()
        db.session.commit()
