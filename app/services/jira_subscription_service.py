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

"""subscription_service.py

Service-helpers for creating and mutating subscription data.
"""

from . import CRUDService, SubscribedJIRAItemService
from .. import db
from ..models import Subscription


class JIRASubscriptionService(CRUDService):
    """CRUD persistent storage service.

    Abstract base class for creating/mutating Subscription data.
    """

    def __init__(self):
        """Creates a new `subscribed_list_service` for the class."""
        self._subscribed_jira_item_service = SubscribedJIRAItemService()

    def create(self, project_key, repo_id, issue_autocard, pull_request_autocard,
               issue_type, issue_keys):
        """Creates and persists a new subscription record to the database.

        Args:
            project_key (str): The key of the `Project` the `Subscription`
                belongs to
            repo_id (int): The id of the `Repo` the `Subscription` belongs to.
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.
            issue_type (JIRAIssueType): An object representing the issue type
                associated with the `Subscription`
            issue_keys (list(str)): An optional list of keys for JIRA issues to
                associate to the subscription as subscribed JIRA issues (or
                projects if an empy string exists in the list)

        Returns:
            None
        """
        if project_key:
            subscription = Subscription(
                project_key=project_key,
                repo_id=repo_id,
                issue_autocard=issue_autocard,
                pull_request_autocard=pull_request_autocard
            )
            db.session.add(subscription)

            # Create all the subscribed lists
            for issue_key in issue_keys:
                self._subscribed_jira_item_service.create(
                    project_key=project_key,
                    repo_id=repo_id,
                    issue_type_id=issue_type,
                    jira_issue_key=issue_key
                )

            # Persists the subscription
            db.session.commit()

    def update(self, project_key, repo_id, issue_autocard, pull_request_autocard):
        """Updates a persisted subscription's autocard value.

        Args:
            project_key (str): The key of the `Project` the `Subscription`
                belongs to
            repo_id (int): The id of the `Repo` the `Subscription` belongs to.
            issue_autocard (Boolean): If `autocard` is `true` for Issues
                created.
            pull_request_autocard (Boolean): If `autocard` is `true` for Pull
                Requests created.

        Returns:
            None
        """
        if project_key:
            subscription = Subscription.query.filter_by(
                project_key=project_key,
                repo_id=repo_id
            ).first()
            subscription.issue_autocard = issue_autocard
            subscription.pull_request_autocard = pull_request_autocard

            # Persist the changes
            db.session.commit()

    def delete(self, project_key, repo_id):
        """Deletes an old, persisted subscription.

        Args:
            project_key (str): The key of the `Project` the `Subscription`
                belongs to
            repo_id (int): The id of the `Repo` the `Subscription` belongs to.

        Returns:
            None
        """
        if project_key:
            subscription = Subscription.query.filter_by(
                project_key=project_key, repo_id=repo_id).first()

            # Delete the record
            db.session.delete(subscription)
            db.session.commit()
