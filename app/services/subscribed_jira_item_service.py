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

"""subscribed_list_service.py

Service-helpers for creating and mutating subscribed_list data.
"""

from . import CRUDService
from .. import db
from ..models import SubscribedJIRAProject, SubscribedJIRAIssue, Project


class SubscribedJIRAItemService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating SubscribedList
    data.
    """

    def create(self, project_key, repo_id, issue_type_id=None, jira_issue_key=None, jira_member_id=None):
        """Creates and persists a subscribed_jira_issue/project record to the database.

        Args:
            project_key (str): The key of the `Project` to raise an issue on
            repo_id (int): The id of the `Repo` the subscribed item belongs
                to.
            issue_type (str): The id of the issue type of the `Project`
                corresponding ot the JIRA issues to be raised on
            jira_issue_key (str): The key of the parent issue for the sub-issues
                raised on
            jira_member_id (str): An optional member id to default assign
                cards created on this subscripion item to.

        Returns:
            None
        """
        if project_key:
            if bool(jira_issue_key):
                project = Project.query.filter_by(key=project_key).first()
                if any(x.name == 'Sub-task' for x in project.issue_types):
                    name = 'Sub-task'
                else:
                    name = 'Subtask'
                subscribed_item = SubscribedJIRAIssue(
                    subscription_project_key=project_key,
                    subscription_repo_id=repo_id,
                    jira_issue_key=jira_issue_key,
                    issue_type_name=name,
                    jira_member_id=jira_member_id
                )
            else:
                subscribed_item = SubscribedJIRAProject(
                    subscription_project_key=project_key,
                    subscription_repo_id=repo_id,
                    issue_type_id=issue_type_id,
                    jira_member_id=jira_member_id
                )

            db.session.add(subscribed_item)

            # Persists the subscribed_item
            db.session.commit()

    def update(self, project_key, repo_id, jira_issue_key=None, jira_member_id=None):
        """Updates a persisted subscribed_jira_issue/project's autocard value.

        Args:
            project_key (str): The key of the `Project` to raise an issue on
            repo_id (int): The id of the `Repo` the subscribed item belongs
                to.
            jira_issue_key (str): The key of the parent issue for the sub-issues
                raised on
            jira_member_id (str): An optional member id to default assign
                cards created on this subscripion item to.

        Returns:
            None
        """
        if project_key:
            if bool(jira_issue_key):
                subscribed_item = SubscribedJIRAIssue.query.get(
                    [project_key, repo_id, jira_issue_key]
                )
            else:
                subscribed_item = SubscribedJIRAProject.query.get(
                    [project_key, repo_id]
                )

            subscribed_item.jira_member_id = jira_member_id

            # Persist the changes
            db.session.commit()

    def delete(self, project_key, repo_id, jira_issue_key=None):
        """Deletes an old, persisted subscribed_jira_issue/project.

        Args:
            project_key (str): The key of the `Project` to raise an issue on
            repo_id (int): The id of the `Repo` the subscribed item belongs
                to.
            jira_issue_key (str): The key of the parent issue for the sub-issues
                raised on

        Returns:
            None
        """
        if project_key:
            if bool(jira_issue_key):
                db.session.delete(
                    SubscribedJIRAIssue.query.get(
                        [project_key, repo_id, jira_issue_key])
                )
            else:
                db.session.delete(
                    SubscribedJIRAProject.query.get(
                        [project_key, repo_id])
                )

            # Persist the changes
            db.session.commit()
